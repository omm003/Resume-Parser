# AI Resume Parser - Local Setup Instructions

Follow these simple steps to run the AI Resume Parser on your local PC:

## Step 1: Install Python
Make sure you have Python 3.8 or newer installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

## Step 2: Set up the project
1. Create a new folder on your computer for the project
2. Place all the files from this package in that folder:
   - app.py
   - resume_parser.py
   - utils.py
   - requirements.txt

## Step 3: Set up a virtual environment (recommended)
Open a command prompt or terminal in your project folder and run:

**Windows:**
```
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```
python -m venv venv
source venv/bin/activate
```

## Step 4: Install dependencies
Run this command to install all required packages:
```
pip install -r requirements.txt
```

## Step 5: Install the spaCy language model
Run this command to download the required language model:
```
python -m spacy download en_core_web_sm
```

## Step 6: Run the application
Start the application with:
```
streamlit run app.py
```

The app will open automatically in your web browser (typically at http://localhost:8501).

## Using the Application
1. Upload PDF or DOCX resume files
2. Click "Parse Resumes" to extract information
3. Navigate to "View Parsed Resumes" to see the results
4. Use "Search Resumes" to find candidates by skills, experience, etc.

## Troubleshooting
- If you see an error about missing packages, run `pip install -r requirements.txt` again
- If the parser fails to recognize information correctly, try uploading a cleaner version of the resume
- For PDF parsing issues, ensure the PDF contains actual text (not just images)

---

If you have any questions or suggestions for improvements, please contact:

**Omm Prakash Pradhan**  
Contact: 8117817687  
Email: ommprakashpradhan1@gmail.com