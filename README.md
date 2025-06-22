# AI Resume Parser

An AI-powered resume parsing system that extracts and organizes key information from resumes to enhance HR processes.

## Features

- Upload PDF/DOCX resumes
- Extract key information including:
  - Basic details (name, email, phone, location)
  - Skills (technical and soft skills)
  - Work experience
  - Education
- View parsed resumes in an organized format
- Search through resumes based on skills, job titles, etc.

## Installation

1. Create a virtual environment (recommended):
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Download the spaCy language model:
   ```
   python -m spacy download en_core_web_sm
   ```

## Running the Application

Run the Streamlit app:
```
streamlit run app.py
```

The application will open in your default web browser at http://localhost:8501

## Usage

1. Navigate to "Upload Resumes" page
2. Upload one or more PDF or DOCX resume files
3. Click "Parse Resumes" to extract information
4. View the parsed information on the "View Parsed Resumes" page
5. Search through resumes using the "Search Resumes" page

## Folder Structure

```
├── app.py              # Main Streamlit application
├── resume_parser.py    # Resume parsing logic
├── utils.py            # Utility functions for extraction
└── requirements.txt    # Required packages
```

## Enhanced Extraction

This version includes improved extraction capabilities for:
- Skills detection with a comprehensive skills database
- Better education information extraction
- More accurate work experience parsing
- Location and contact information detection

---

## Developed by
**Omm Prakash Pradhan**  
Contact: 8117817687  
Email: ommprakashpradhan1@gmail.com

## License
[BSD-3-Clause](LICENSE)