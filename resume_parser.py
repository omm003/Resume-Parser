import re
import os
import spacy
import pdfplumber
import docx
from utils import extract_skills, extract_phone_number, extract_email, extract_linkedin

class ResumeParser:
    def __init__(self, resume_path):
        self.resume_path = resume_path
        self.text = self._extract_text()
        
        # Load spaCy NLP model
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If model isn't downloaded, inform user to download it
            raise ImportError(
                "Spacy model 'en_core_web_sm' not found. Please install it using: python -m spacy download en_core_web_sm"
            )
    
    def _extract_text(self):
        """Extract text from resume based on file extension"""
        file_extension = os.path.splitext(self.resume_path)[1].lower()
        
        if file_extension == '.pdf':
            return self._extract_text_from_pdf()
        elif file_extension == '.docx':
            return self._extract_text_from_docx()
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_text_from_pdf(self):
        """Extract text from PDF files"""
        try:
            text = ""
            with pdfplumber.open(self.resume_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            
            if not text.strip():
                raise ValueError("No text could be extracted from the PDF. It might be scanned or protected.")
            
            return text
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {str(e)}")
    
    def _extract_text_from_docx(self):
        """Extract text from DOCX files"""
        try:
            doc = docx.Document(self.resume_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            if not text.strip():
                raise ValueError("No text could be extracted from the DOCX file.")
            
            return text
        except Exception as e:
            raise ValueError(f"Error extracting text from DOCX: {str(e)}")
    
    def _extract_name(self, doc):
        """Extract name from the resume using advanced NLP and pattern matching"""
        # Method 1: Using NER to find PERSON entities
        person_entities = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
        
        # Often the first person mentioned is the candidate
        if person_entities:
            # Preference for names with 2+ words (first and last name)
            full_names = [name for name in person_entities if len(name.split()) >= 2]
            if full_names:
                return full_names[0]
            return person_entities[0]
        
        # Method 2: Look for common name patterns at the beginning of resumes
        lines = self.text.strip().split('\n')
        
        # Check first 5 lines for potential names
        for i in range(min(5, len(lines))):
            line = lines[i].strip()
            
            # Skip lines that are clearly headers or too long to be names
            if any(title in line.lower() for title in ["resume", "cv", "curriculum", "vitae", "profile"]):
                continue
                
            # Good candidates are lines with 2-4 words, properly capitalized
            words = line.split()
            if 2 <= len(words) <= 4:
                # Check if words look like names (capitalized, not all caps)
                if all(word[0].isupper() and not word.isupper() for word in words if len(word) > 1):
                    return line
        
        # Method 3: Look for lines with name indicators
        name_patterns = [
            r"(?i)name\s*[:;-]?\s*([A-Z][a-z]+(?: [A-Z][a-z]+){1,3})",
            r"(?i)(?:^|\n)([A-Z][a-z]+(?: [A-Z][a-z]+){1,3})(?:\n|$)",
            r"(?:^|\n)([A-Z][a-zA-Z]+(?: [A-Z][a-zA-Z]+){1,3})\s*\n"
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, self.text)
            if matches:
                return matches[0]
        
        # Method 4: Simple fallback - first line if it's short
        first_line = lines[0].strip()
        if len(first_line.split()) <= 5:
            return first_line
        
        return "Not found"
    
    def _extract_education(self, doc):
        """Extract education information from the resume with enhanced CGPA detection"""
        education = []
        
        # Find education section
        education_keywords = ["education", "academic", "qualification", "degree", "university", "college", "school"]
        education_section = self._find_section("education", education_keywords)
        
        if not education_section:
            # If no dedicated section found, scan entire resume for education-related content
            education_patterns = [
                r"(?i)(?:(?:19|20)\d{2}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[^\n]*(?:university|college|institute|school)[^\n]*(?:degree|bachelor|master|phd|diploma)[^\n]*",
                r"(?i)(?:university|college|institute|school)[^\n]*(?:degree|bachelor|master|phd|diploma)[^\n]*(?:(?:19|20)\d{2}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[^\n]*"
            ]
            
            for pattern in education_patterns:
                matches = re.findall(pattern, self.text)
                if matches:
                    education_section = "\n".join(matches)
                    break
                    
            if not education_section:
                return []
        
        # Parse education entries
        lines = education_section.split("\n")
        current_entry = {}
        
        # Enhanced patterns
        institution_pattern = r"(?i)((?:university|college|institute|school|academy)(?:[^,\n]*)?)"
        degree_pattern = r"(?i)(bachelor|master|phd|diploma|certification|b\.?(?:sc|a|e|tech|s)|m\.?(?:sc|a|tech|s)|doctorate|associate|graduate|undergraduate)"
        date_pattern = r"(?i)((?:19|20)\d{2})\s*[-–—]?\s*(?:((?:19|20)\d{2})|present|current|now)?"
        
        # Comprehensive GPA/CGPA patterns
        gpa_patterns = [
            r"(?i)(?:gpa|grade point average)[:\s]*([\d\.]+)(?:\s*\/\s*[\d\.]+)?",
            r"(?i)(?:cgpa|cumulative grade point average)[:\s]*([\d\.]+)(?:\s*\/\s*[\d\.]+)?",
            r"(?i)(?:percentage|marks|score)[:\s]*([\d\.]+)\s*%?",
            r"(?i)with\s+(?:a\s+)?(?:gpa|cgpa)\s+(?:of\s+)?([\d\.]+)",
            r"(?i)(?:obtained|achieved|secured|with)[:\s]*(?:a\s+)?(?:score|percentage|marks)[:\s]*([\d\.]+)\s*%?",
            r"(?i)(?:grades?|marks)[:\s]*([\d\.]+)[^\d\.\/]*(?:\/|of|out of)[\s]*([\d\.]+)",
            r"(?i)(?:first class|second class|distinction|merit)[^\d]*?([\d\.]+)\s*%?"
        ]
        
        # Method 1: Structured pattern extraction
        for i, line in enumerate(lines):
            # Look for institution/university
            institution_match = re.search(institution_pattern, line, re.IGNORECASE)
            if institution_match:
                # If we already have a partial entry, save it before starting a new one
                if current_entry and "institution" in current_entry:
                    education.append(current_entry)
                    current_entry = {}
                
                current_entry["institution"] = institution_match.group(0).strip()
                
                # Check for degree in same line
                degree_match = re.search(degree_pattern, line, re.IGNORECASE)
                if degree_match:
                    current_entry["degree"] = degree_match.group(0).strip()
                
                # Check for dates in same line
                date_match = re.search(date_pattern, line, re.IGNORECASE)
                if date_match:
                    start_date = date_match.group(1)
                    end_date = date_match.group(2) if date_match.group(2) else "Present"
                    current_entry["date"] = f"{start_date} - {end_date}"
                
                # Check GPA/scores in this line and potentially next few lines
                score_found = False
                for j in range(i, min(i+3, len(lines))):
                    for pattern in gpa_patterns:
                        score_match = re.search(pattern, lines[j], re.IGNORECASE)
                        if score_match:
                            # Extract the numeric part, handling different formats
                            score_value = score_match.group(1)
                            # Check if this is out of a standard scale (like 4.0 or 10.0)
                            score_denominator = score_match.group(2) if len(score_match.groups()) > 1 and score_match.group(2) else None
                            
                            if score_denominator:
                                current_entry["score"] = f"{score_value}/{score_denominator}"
                            else:
                                # Try to determine if this is percentage or GPA
                                if float(score_value) > 10:
                                    current_entry["score"] = f"{score_value}%"
                                else:
                                    current_entry["score"] = score_value
                            
                            score_found = True
                            break
                    
                    if score_found:
                        break
            
            # If no institution found in this line, check if we have a current entry to update
            elif current_entry and "institution" in current_entry:
                # Look for degree if not already found
                if "degree" not in current_entry:
                    degree_match = re.search(degree_pattern, line, re.IGNORECASE)
                    if degree_match:
                        current_entry["degree"] = degree_match.group(0).strip()
                
                # Look for dates if not already found
                if "date" not in current_entry:
                    date_match = re.search(date_pattern, line, re.IGNORECASE)
                    if date_match:
                        start_date = date_match.group(1)
                        end_date = date_match.group(2) if date_match.group(2) else "Present"
                        current_entry["date"] = f"{start_date} - {end_date}"
                
                # Look for GPA/scores if not already found
                if "score" not in current_entry:
                    for pattern in gpa_patterns:
                        score_match = re.search(pattern, line, re.IGNORECASE)
                        if score_match:
                            score_value = score_match.group(1)
                            # Check if this is out of a standard scale
                            score_denominator = score_match.group(2) if len(score_match.groups()) > 1 and score_match.group(2) else None
                            
                            if score_denominator:
                                current_entry["score"] = f"{score_value}/{score_denominator}"
                            else:
                                # Try to determine if this is percentage or GPA
                                try:
                                    if float(score_value) > 10:
                                        current_entry["score"] = f"{score_value}%"
                                    else:
                                        current_entry["score"] = score_value
                                except ValueError:
                                    current_entry["score"] = score_value
                            break
        
        # Save the last entry if exists
        if current_entry and "institution" in current_entry:
            # Add defaults for missing fields
            if "degree" not in current_entry:
                current_entry["degree"] = "Degree not specified"
            if "date" not in current_entry:
                current_entry["date"] = "Date not specified"
            if "score" not in current_entry:
                current_entry["score"] = "Not specified"
                
            education.append(current_entry)
        
        # If we still didn't find any education entries, try a more aggressive approach
        if not education:
            # Look for any mentions of educational institutions
            for line in lines:
                if re.search(r"(?i)(?:university|college|institute|school|academy)", line):
                    # Extract the institution name with some context
                    institution = line.strip()
                    
                    # Look for degree info
                    degree_match = re.search(degree_pattern, line, re.IGNORECASE)
                    degree = degree_match.group(0) if degree_match else "Degree not specified"
                    
                    # Look for dates
                    date_match = re.search(date_pattern, line, re.IGNORECASE)
                    date = "Date not specified"
                    if date_match:
                        start_date = date_match.group(1)
                        end_date = date_match.group(2) if date_match.group(2) else "Present"
                        date = f"{start_date} - {end_date}"
                    
                    # Look for GPA
                    score = "Not specified"
                    for pattern in gpa_patterns:
                        score_match = re.search(pattern, line, re.IGNORECASE)
                        if score_match:
                            score = score_match.group(1)
                            break
                    
                    education.append({
                        "institution": institution,
                        "degree": degree,
                        "date": date,
                        "score": score
                    })
        
        return education
    
    def _extract_experience(self, doc):
        """Extract work experience information from the resume"""
        experience = []
        
        # Find experience section
        experience_keywords = ["experience", "employment", "work history", "professional background", "career"]
        experience_section = self._find_section("experience", experience_keywords)
        
        if not experience_section:
            return []
        
        # Extract potential work experience entries
        # Look for patterns like "Company Name (2019-2022)" or "2019-2022: Company Name"
        company_pattern = r"(?i)((?:19|20)\d{2})\s*[-–—]?\s*(?:((?:19|20)\d{2})|present|current|now)?\s*(.+?)(?:\n|$)"
        
        # Look for work experience entries
        for match in re.finditer(company_pattern, experience_section, re.MULTILINE):
            start_date, end_date, company_text = match.groups()
            
            # Try to separate job title and company
            parts = company_text.split(',', 1)
            if len(parts) >= 2:
                title, company = parts[0].strip(), parts[1].strip()
            else:
                # If no comma, try to make an educated guess
                title_match = re.search(r"(?i)(engineer|developer|manager|director|analyst|specialist|consultant|designer)", company_text)
                if title_match:
                    index = title_match.start()
                    title = company_text[index:].strip()
                    company = company_text[:index].strip()
                else:
                    title = "Position not specified"
                    company = company_text.strip()
            
            # Format date
            date = f"{start_date} - {end_date if end_date else 'Present'}"
            
            # Get description if available (usually follows the job entry)
            next_block = experience_section[match.end():].split('\n\n', 1)[0] if match.end() < len(experience_section) else ""
            description = next_block.strip() if next_block and not re.match(company_pattern, next_block) else "No description available"
            
            experience.append({
                "company": company,
                "title": title,
                "date": date,
                "description": description
            })
        
        return experience
    
    def _find_section(self, section_name, keywords):
        """Find and extract a specific section from the resume text"""
        for keyword in keywords:
            # Look for section headers
            pattern = rf"(?i)(?:^|\n)[ \t]*(?:{keyword})[ \t]*(?::|$)[ \t]*\n"
            match = re.search(pattern, self.text)
            
            if match:
                # Found a section, now extract everything up to the next section header
                start_idx = match.end()
                
                # Find the next section header (if any)
                next_section = re.search(r"(?i)(?:^|\n)[ \t]*(?:education|experience|skills|projects|certifications|summary|objective)[ \t]*(?::|$)[ \t]*\n", self.text[start_idx:])
                
                if next_section:
                    end_idx = start_idx + next_section.start()
                    return self.text[start_idx:end_idx].strip()
                else:
                    return self.text[start_idx:].strip()
        
        # Section not found
        return ""
    
    def _extract_location(self, doc):
        """Extract location information from the resume"""
        for ent in doc.ents:
            if ent.label_ in ["GPE", "LOC"]:
                return ent.text
        
        # Fallback: Look for common address patterns
        address_pattern = r"(?i)(?:address|location|residing at|based in)(?:[:\s]+)([A-Za-z0-9\s,.]+(?:road|street|ave|avenue|blvd|boulevard|city|town|state|zip|zipcode|postal code)[A-Za-z0-9\s,.]+)"
        match = re.search(address_pattern, self.text)
        if match:
            return match.group(1).strip()
        
        return "Not found"
    
    def parse(self):
        """Parse the resume and extract relevant information"""
        doc = self.nlp(self.text)
        
        # Extract basic information
        parsed_data = {
            "name": self._extract_name(doc),
            "email": extract_email(self.text),
            "phone": extract_phone_number(self.text),
            "linkedin": extract_linkedin(self.text),
            "location": self._extract_location(doc),
            "skills": extract_skills(self.text),
            "education": self._extract_education(doc),
            "experience": self._extract_experience(doc)
        }
        
        return parsed_data