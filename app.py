import streamlit as st
import fitz
from docx import Document


# ---------- Page Setup ----------
st.set_page_config(page_title="SkillGap AI")

st.title("SkillGap AI")
st.subheader("AI-powered Resume & Job Description Analyzer")

st.write(
    "Compare a resume with a job description to identify matching and missing skills."
)


# ---------- Resume Text Extraction ----------
def extract_resume_text(uploaded_file):
    file_type = uploaded_file.name.lower()

    if file_type.endswith(".pdf"):
        document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        text = ""
        for page in document:
            text += page.get_text()

        document.close()
        return text

    elif file_type.endswith(".docx"):
        document = Document(uploaded_file)

        text = ""
        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    else:
        raise ValueError("Unsupported file type.")


# ---------- User Input ----------
resume_file = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

job_description = st.text_area(
    "Job description",
    height=300,
    placeholder="Paste the job description here..."
)


# ---------- Analysis ----------
if st.button("Analyze Resume"):

    if not resume_file and not job_description.strip():
        st.warning("Please upload a resume and enter a job description.")

    elif not resume_file:
        st.warning("Please upload a resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            resume_text = extract_resume_text(resume_file)

            if not resume_text.strip():
                st.error("Could not extract any text from the resume.")
            else:
                st.subheader("Extracted Resume Text")
                st.text_area(
                    "Resume content",
                    resume_text,
                    height=400
                )

        except Exception as e:
            st.error(f"Error extracting resume text: {e}")