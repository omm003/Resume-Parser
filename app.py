import streamlit as st
import os
import pandas as pd
import tempfile
from resume_parser import ResumeParser

# Set page configuration
st.set_page_config(
    page_title="AI Resume Parser",
    page_icon="📄",
    layout="wide"
)

# Initialize session state for storing parsed resumes
if 'parsed_resumes' not in st.session_state:
    st.session_state.parsed_resumes = []

def save_uploaded_file(uploaded_file):
    """Save uploaded file to a temporary location and return the path"""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
            tmp.write(uploaded_file.getvalue())
            return tmp.name
    except Exception as e:
        st.error(f"Error saving uploaded file: {e}")
        return None

def main():
    st.title("AI Resume Parser")
    st.write("Upload resumes to extract key information for HR processes")
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload Resumes", "View Parsed Resumes", "Search Resumes"])
    
    if page == "Upload Resumes":
        show_upload_page()
    elif page == "View Parsed Resumes":
        show_parsed_resumes()
    elif page == "Search Resumes":
        search_resumes()
    
    # Footer with credits
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### Developed by:
    **Omm Prakash Pradhan**  
    Contact: 8117817687  
    Email: ommprakashpradhan1@gmail.com
    """)

def show_upload_page():
    st.header("Upload Resumes")
    
    uploaded_files = st.file_uploader(
        "Upload resume files (PDF/DOCX)", 
        type=["pdf", "docx"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Parse Resumes"):
            with st.spinner("Parsing resumes..."):
                for uploaded_file in uploaded_files:
                    # Save the file to a temporary location
                    temp_file_path = save_uploaded_file(uploaded_file)
                    
                    if temp_file_path:
                        try:
                            # Parse the resume
                            parser = ResumeParser(temp_file_path)
                            parsed_data = parser.parse()
                            
                            # Add the file name to the parsed data
                            parsed_data['file_name'] = uploaded_file.name
                            
                            # Add the parsed resume to session state
                            st.session_state.parsed_resumes.append(parsed_data)
                            
                            # Display success message
                            st.success(f"Successfully parsed {uploaded_file.name}")
                            
                            # Clean up the temporary file
                            os.unlink(temp_file_path)
                        except Exception as e:
                            st.error(f"Failed to parse {uploaded_file.name}: {str(e)}")
                            # Clean up the temporary file
                            if os.path.exists(temp_file_path):
                                os.unlink(temp_file_path)
                
                st.success("All resumes processed successfully!")
                st.write(f"Total resumes parsed: {len(st.session_state.parsed_resumes)}")

def show_parsed_resumes():
    st.header("View Parsed Resumes")
    
    if not st.session_state.parsed_resumes:
        st.info("No resumes have been parsed yet. Please upload and parse resumes first.")
        return
    
    # Display parsed resumes in a selectable format
    resume_names = [resume['file_name'] for resume in st.session_state.parsed_resumes]
    selected_resume = st.selectbox("Select a resume to view", resume_names)
    
    # Find the selected resume in session state
    selected_resume_data = next((resume for resume in st.session_state.parsed_resumes 
                               if resume['file_name'] == selected_resume), None)
    
    if selected_resume_data:
        display_resume_info(selected_resume_data)

def display_resume_info(resume_data):
    """Display parsed resume information in an organized format"""
    st.subheader("Basic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write(f"**Name:** {resume_data.get('name', 'Not found')}")
        st.write(f"**Email:** {resume_data.get('email', 'Not found')}")
        st.write(f"**Phone:** {resume_data.get('phone', 'Not found')}")
    
    with col2:
        st.write(f"**Location:** {resume_data.get('location', 'Not found')}")
        st.write(f"**LinkedIn:** {resume_data.get('linkedin', 'Not found')}")
    
    st.subheader("Skills")
    skills = resume_data.get('skills', [])
    if skills:
        # Display skills as colorful tags
        skills_html = ""
        colors = ["#4CAF50", "#2196F3", "#FF9800", "#E91E63", "#9C27B0"]  # Green, Blue, Orange, Pink, Purple
        
        for i, skill in enumerate(skills):
            color = colors[i % len(colors)]
            skills_html += f'<span style="background-color: {color}; color: white; padding: 5px 10px; margin: 3px; border-radius: 15px; display: inline-block; font-weight: 500;">{skill}</span>'
        
        st.markdown(skills_html, unsafe_allow_html=True)
    else:
        st.write("No skills found")
    
    st.subheader("Work Experience")
    experiences = resume_data.get('experience', [])
    if experiences:
        for idx, exp in enumerate(experiences):
            with st.expander(f"{exp.get('title', 'Role')} at {exp.get('company', 'Company')}"):
                st.write(f"**Period:** {exp.get('date', 'Not specified')}")
                st.write(f"**Description:** {exp.get('description', 'No description available')}")
    else:
        st.write("No work experience found")
    
    st.subheader("Education")
    education = resume_data.get('education', [])
    if education:
        for idx, edu in enumerate(education):
            with st.expander(f"{edu.get('degree', 'Degree')} from {edu.get('institution', 'Institution')}"):
                st.write(f"**Period:** {edu.get('date', 'Not specified')}")
                st.write(f"**GPA/Scores:** {edu.get('score', 'Not specified')}")
    else:
        st.write("No education information found")

def search_resumes():
    st.header("Search Resumes")
    
    if not st.session_state.parsed_resumes:
        st.info("No resumes have been parsed yet. Please upload and parse resumes first.")
        return
    
    search_term = st.text_input("Enter search term (skill, job title, company, etc.)")
    
    if search_term:
        search_results = []
        
        for resume in st.session_state.parsed_resumes:
            score = 0
            matches = []
            
            # Check for matches in name
            if search_term.lower() in resume.get('name', '').lower():
                score += 10
                matches.append(f"Name contains '{search_term}'")
            
            # Check for matches in skills
            skills = resume.get('skills', [])
            for skill in skills:
                if search_term.lower() in skill.lower():
                    score += 5
                    matches.append(f"Skill matched: '{skill}'")
            
            # Check for matches in experience
            experiences = resume.get('experience', [])
            for exp in experiences:
                if (search_term.lower() in exp.get('title', '').lower() or
                    search_term.lower() in exp.get('company', '').lower() or
                    search_term.lower() in exp.get('description', '').lower()):
                    score += 3
                    matches.append(f"Experience matched: {exp.get('title', 'Role')} at {exp.get('company', 'Company')}")
            
            # Check for matches in education
            education = resume.get('education', [])
            for edu in education:
                if (search_term.lower() in edu.get('degree', '').lower() or
                    search_term.lower() in edu.get('institution', '').lower()):
                    score += 2
                    matches.append(f"Education matched: {edu.get('degree', 'Degree')} from {edu.get('institution', 'Institution')}")
            
            if score > 0:
                search_results.append({
                    'file_name': resume['file_name'],
                    'name': resume.get('name', 'Unknown'),
                    'score': score,
                    'matches': matches,
                    'full_data': resume
                })
        
        if search_results:
            # Sort results by score (highest first)
            search_results.sort(key=lambda x: x['score'], reverse=True)
            
            st.subheader(f"Found {len(search_results)} matching resumes")
            
            for idx, result in enumerate(search_results):
                with st.expander(f"{result['name']} - {result['file_name']} (Match score: {result['score']})"):
                    st.write("**Matched on:**")
                    for match in result['matches']:
                        st.write(f"- {match}")
                    
                    st.write("---")
                    st.write("**Resume details:**")
                    display_resume_info(result['full_data'])
        else:
            st.info(f"No resumes found matching '{search_term}'")

if __name__ == "__main__":
    main()