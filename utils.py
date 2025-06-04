import re
import spacy
from spacy.matcher import Matcher

# Load skills database
def load_skills():
    """Load a comprehensive list of technical and soft skills"""
    technical_skills = [
        # Programming Languages
        "python", "java", "javascript", "c++", "c#", "ruby", "php", "swift", "kotlin", "go", "rust", "typescript",
        "scala", "perl", "r", "matlab", "bash", "shell", "powershell", "dart", "objective-c", "visual basic",
        "golang", "assembly", "fortran", "cobol", "pl/sql", "haskell", "clojure", "groovy", "lua", "erlang", "elixir",
        # Frontend Technologies
        "html", "css", "html5", "css3", "sass", "less", "bootstrap", "tailwind", "material-ui", "material design", 
        "react", "reactjs", "react.js", "vue", "vuejs", "vue.js", "angular", "angularjs", "angular.js", "jquery",
        "redux", "svelte", "ember", "backbone", "next.js", "nuxt.js", "gatsby", "webpack", "babel", "typescript",
        "responsive design", "progressive web apps", "pwa", "web components", "web accessibility", "wcag",
        # Backend Technologies
        "node.js", "express", "django", "flask", "fastapi", "spring", "spring boot", "hibernate", "asp.net",
        "laravel", "ruby on rails", "rails", "phoenix", "play framework", "symfony", "codeigniter", "struts",
        "jsp", "servlet", "graphql", "rest api", "soap", "oauth", "jwt", "websocket", "grpc", "microservices",
        "serverless", "lambda", "api gateway", "restful", "api development", "middleware", "nestjs", "next.js",
        # Databases
        "sql", "mysql", "postgresql", "postgres", "mongodb", "oracle", "sqlite", "nosql", "redis", "firebase",
        "dynamodb", "cassandra", "mariadb", "elasticsearch", "neo4j", "couchdb", "db2", "microsoft sql server",
        "ms sql", "rdbms", "acid", "database design", "data modeling", "normalization", "denormalization",
        "indexing", "query optimization", "orm", "database migration", "etl", "data warehousing", "data lake",
        # Cloud & DevOps
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud", "cloud computing",
        "docker", "kubernetes", "jenkins", "ci/cd", "continuous integration", "continuous deployment",
        "terraform", "ansible", "puppet", "chef", "git", "github", "gitlab", "bitbucket", "jira", "confluence",
        "devops", "devsecops", "infrastructure as code", "iac", "vagrant", "virtualbox", "vmware", "openstack",
        "networking", "load balancing", "auto scaling", "fault tolerance", "high availability", "disaster recovery",
        "monitoring", "logging", "prometheus", "grafana", "elk stack", "cloud architecture", "cloud security",
        # Data Science & AI
        "machine learning", "deep learning", "artificial intelligence", "ai", "nlp", "natural language processing", 
        "computer vision", "data science", "data analytics", "data mining", "pandas", "numpy", "scikit-learn", 
        "tensorflow", "pytorch", "keras", "opencv", "tableau", "power bi", "data visualization", "big data", "spark",
        "hadoop", "data warehousing", "etl", "statistics", "probability", "linear algebra", "calculus",
        "regression", "classification", "clustering", "neural networks", "cnn", "rnn", "lstm", "gan", "reinforcement learning",
        "forecasting", "time series analysis", "feature engineering", "model training", "hyperparameter tuning",
        "a/b testing", "experimental design", "predictive modeling", "recommendation systems", "sentiment analysis",
        # Mobile
        "android", "ios", "react native", "flutter", "xamarin", "ionic", "swift", "kotlin", "objective-c",
        "mobile development", "responsive design", "pwa", "progressive web apps", "mobile ui", "native development",
        "cross-platform development", "mobile testing", "app store", "play store", "mobile security",
        # Security
        "cybersecurity", "network security", "information security", "penetration testing", "pen testing",
        "vulnerability assessment", "ethical hacking", "security auditing", "cryptography", "encryption",
        "authentication", "authorization", "oauth", "jwt", "sso", "single sign-on", "iam", "identity management",
        "security protocols", "firewall", "ids", "ips", "vpn", "ssl", "tls", "https", "security compliance",
        # Project Management
        "agile", "scrum", "kanban", "waterfall", "lean", "prince2", "pmi", "pmp", "project coordination",
        "sprint planning", "stakeholder management", "risk management", "resource allocation", "budgeting",
        "gantt chart", "jira", "asana", "trello", "basecamp", "project scheduling", "milestone tracking",
        # Testing
        "unit testing", "integration testing", "functional testing", "system testing", "acceptance testing",
        "regression testing", "tdd", "bdd", "test automation", "selenium", "cypress", "jest", "mocha", "junit",
        "pytest", "testng", "katalon", "postman", "soapui", "qa", "quality assurance", "test planning",
        "test case design", "test execution", "bug tracking", "defect management", "load testing", "performance testing",
        # Other Technical Skills
        "blockchain", "big data", "iot", "internet of things", "embedded systems", "virtual reality", "vr",
        "augmented reality", "ar", "game development", "unity", "unreal engine", "web3", "smart contracts",
        "solidity", "nft", "crypto", "distributed systems", "parallel computing", "quantum computing"
    ]
    
    soft_skills = [
        # Communication Skills
        "communication", "verbal communication", "written communication", "public speaking", "presentation skills",
        "listening", "active listening", "interpersonal communication", "technical writing", "documentation",
        "articulate", "persuasion", "negotiation", "conflict resolution", "storytelling", "public relations",
        # Interpersonal Skills
        "teamwork", "collaboration", "interpersonal skills", "relationship building", "networking", "empathy",
        "emotional intelligence", "cultural awareness", "diversity awareness", "mentoring", "coaching", "training",
        "social skills", "diplomacy", "patience", "respect", "team player", "rapport building", "inclusivity",
        # Leadership Skills
        "leadership", "team leadership", "people management", "strategic leadership", "visionary leadership",
        "delegation", "motivation", "inspiration", "influence", "decision making", "strategic thinking",
        "executive presence", "accountability", "initiative", "ownership", "supervision", "team building",
        # Problem Solving Skills
        "problem solving", "critical thinking", "analytical thinking", "logical reasoning", "troubleshooting",
        "root cause analysis", "systems thinking", "innovation", "creativity", "design thinking", "abstract thinking",
        "debugging", "attention to detail", "research", "investigation", "deductive reasoning", "inductive reasoning",
        # Time Management Skills
        "time management", "prioritization", "organization", "planning", "multitasking", "efficiency", "productivity",
        "self-management", "punctuality", "deadline management", "goal setting", "scheduling", "work ethic",
        # Adaptability Skills
        "adaptability", "flexibility", "resilience", "agility", "learning agility", "change management",
        "stress management", "crisis management", "persistence", "resourcefulness", "improvisation", "curiosity",
        # Business Skills
        "business acumen", "strategic planning", "commercial awareness", "entrepreneurship", "financial literacy",
        "budgeting", "cost analysis", "market research", "marketing", "sales", "customer service", 
        "client relationship management", "compliance", "contract management", "negotiation", "operations",
        # Other Soft Skills
        "attention to detail", "detail-oriented", "accuracy", "precision", "thoroughness", "self-motivation",
        "enthusiasm", "positivity", "confidence", "reliability", "dependability", "trustworthiness", "integrity",
        "ethics", "professionalism", "discretion", "confidentiality", "work-life balance", "continuous learning"
    ]
    
    return set(technical_skills + soft_skills)

def extract_skills(text):
    """Extract skills from resume text using enhanced methods"""
    skills_dict = load_skills()
    found_skills = set()
    
    # Convert text to lowercase for matching
    text_lower = text.lower()
    
    # Method 1: Check for exact skill mentions with word boundaries
    for skill in skills_dict:
        # Use word boundary for more accurate matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill.title())  # Store with proper capitalization
    
    # Method 2: Look for skills in skills section specifically
    skills_section = ""
    skills_headers = ["skills", "technical skills", "core competencies", "competencies", "areas of expertise", "key skills"]
    
    for header in skills_headers:
        pattern = rf"(?i)(?:^|\n)\s*{re.escape(header)}(?:\s*:|$)\s*\n"
        match = re.search(pattern, text)
        if match:
            # Find the end of the skills section (next section header or end of text)
            start_idx = match.end()
            next_section = re.search(r"(?i)(?:^|\n)\s*(?:education|experience|projects|certifications|summary|objective|professional background|work history|employment)\s*(?::|$)", text[start_idx:])
            
            if next_section:
                end_idx = start_idx + next_section.start()
                skills_section = text[start_idx:end_idx]
            else:
                skills_section = text[start_idx:]
                
            # Found a skills section, no need to look further
            break
    
    if skills_section:
        # Look for bulleted or comma-separated skills
        # Handle bullet points (•, -, *, etc.)
        bullet_skills = re.findall(r'(?:^|\n)[•\-\*]\s*([^\n•\-\*]+)', skills_section)
        for skill_text in bullet_skills:
            # For each bulleted item, check if it contains known skills
            for skill in skills_dict:
                if re.search(r'\b' + re.escape(skill) + r'\b', skill_text.lower()):
                    found_skills.add(skill.title())
        
        # Handle comma-separated skills
        comma_sections = re.findall(r'(?:^|\n)([^•\-\*\n][^\n]+)', skills_section)
        for section in comma_sections:
            skill_candidates = [s.strip() for s in section.split(',')]
            for candidate in skill_candidates:
                # Check each comma-separated item against our skills dictionary
                candidate_lower = candidate.lower()
                for skill in skills_dict:
                    if re.search(r'\b' + re.escape(skill) + r'\b', candidate_lower):
                        found_skills.add(skill.title())
    
    # Method 3: Check for programming language patterns specifically
    programming_pattern = r'(?i)(?:proficient|experienced|skilled|fluent)\s+in\s+([^.]+)'
    programming_matches = re.findall(programming_pattern, text)
    for match in programming_matches:
        for skill in skills_dict:
            if re.search(r'\b' + re.escape(skill) + r'\b', match.lower()):
                found_skills.add(skill.title())
    
    return list(found_skills)

def extract_phone_number(text):
    """Extract phone number from text with enhanced pattern recognition"""
    # Common phone number patterns
    patterns = [
        r'(?:\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # (123) 456-7890 or +1 (123) 456-7890
        r'(?:\+\d{1,3}[-.\s]?)?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # 123-456-7890 or +1 123-456-7890
        r'(?:\+\d{1,3}[-.\s]?)?\d{5}[-.\s]?\d{5,6}',  # +91 12345 67890 (Indian format)
        r'(?:\+\d{1,3}[-.\s]?)?\d{4}[-.\s]?\d{3}[-.\s]?\d{3}'   # +44 1234 567 890 (UK format)
    ]
    
    # Look for contextual indicators that often appear near phone numbers
    context_patterns = [
        r'(?i)(?:phone|mobile|cell|tel|telephone|contact)(?:\s*[:;-])?\s*(\+?(?:\d[-\.\s]?){7,15}\d)',
        r'(?i)(?:phone|mobile|cell|tel|telephone|contact)[^\n]*?(\+?(?:\d[-\.\s]?){7,15}\d)'
    ]
    
    # Check context patterns first (more likely to get the right number with context)
    for pattern in context_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    # Fall back to standard patterns
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    
    return "Not found"

def extract_email(text):
    """Extract email address from text with enhanced context recognition"""
    # Standard email pattern
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Look for contextual indicators that often appear near emails
    context_patterns = [
        r'(?i)(?:email|e-mail|mail|contact)(?:\s*[:;-])?\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        r'(?i)(?:email|e-mail|mail|contact)[^\n]*?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
    ]
    
    # Check context patterns first
    for pattern in context_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    # Fall back to standard pattern
    match = re.search(email_pattern, text)
    if match:
        return match.group(0)
    
    return "Not found"

def extract_linkedin(text):
    """Extract LinkedIn profile URL from text with enhanced recognition"""
    # LinkedIn patterns
    linkedin_patterns = [
        r'linkedin\.com/in/[a-zA-Z0-9_-]+/?',
        r'linkedin\.com/profile/[a-zA-Z0-9_-]+/?',
        r'linkedin\.com/pub/[a-zA-Z0-9_-]+/?'
    ]
    
    # Context patterns
    context_patterns = [
        r'(?i)(?:linkedin|linked\s*in|profile)(?:\s*[:;-])?\s*((?:https?://)?(?:www\.)?linkedin\.com/(?:in|profile|pub)/[a-zA-Z0-9_-]+/?)',
        r'(?i)(?:linkedin|linked\s*in|profile)[^\n]*?((?:https?://)?(?:www\.)?linkedin\.com/(?:in|profile|pub)/[a-zA-Z0-9_-]+/?)'
    ]
    
    # Check context patterns first
    for pattern in context_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    
    # Fall back to standard patterns
    for pattern in linkedin_patterns:
        match = re.search(pattern, text)
        if match:
            # Extract the full URL if available
            full_url = text[max(0, match.start()-20):match.end()+20]
            url_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/(?:in|profile|pub)/[a-zA-Z0-9_-]+/?'
            full_match = re.search(url_pattern, full_url)
            if full_match:
                return full_match.group(0)
            return match.group(0)
    
    return "Not found"

# Additional utility functions for enhancing resume parsing

def extract_project_info(text):
    """Extract project information from a resume"""
    projects = []
    
    # Find projects section
    project_keywords = ["projects", "personal projects", "academic projects", "key projects", "relevant projects"]
    
    # Try to find the projects section
    project_section = ""
    for keyword in project_keywords:
        pattern = rf"(?i)(?:^|\n)\s*{re.escape(keyword)}(?:\s*:|$)\s*\n"
        match = re.search(pattern, text)
        if match:
            start_idx = match.end()
            next_section = re.search(r"(?i)(?:^|\n)\s*(?:education|experience|skills|certifications|summary|objective|awards)\s*(?::|$)", text[start_idx:])
            
            if next_section:
                end_idx = start_idx + next_section.start()
                project_section = text[start_idx:end_idx]
            else:
                project_section = text[start_idx:]
            
            break
    
    if project_section:
        # Look for project entries - typically start with a project name or bullet
        project_entries = re.split(r'(?:^|\n)(?:[-•*]\s*|\d+\.\s+|(?:[A-Z][a-zA-Z0-9]+ )+:)', project_section)
        project_entries = [entry for entry in project_entries if entry.strip()]
        
        for entry in project_entries:
            # Try to identify project name
            lines = entry.split('\n')
            project_name = lines[0].strip() if lines else "Unnamed Project"
            
            # Look for technologies used
            tech_match = re.search(r'(?i)(?:technologies|tech stack|tools|languages)(?:\s*used)?(?:\s*:|;)?\s*([^.]+)', entry)
            technologies = tech_match.group(1).strip() if tech_match else "Not specified"
            
            # Rest is description
            description = entry
            
            projects.append({
                "name": project_name,
                "technologies": technologies,
                "description": description
            })
    
    return projects