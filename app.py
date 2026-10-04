import streamlit as st


# Set up the page.
st.set_page_config(page_title="SkillGap AI")

# Introduce the application.
st.title("SkillGap AI")
st.subheader("AI-powered Resume & Job Description Analyzer")
st.write(
	"Compare a resume with a job description to identify matching and missing skills."
)

# Collect the resume and job description.
resume_file = st.file_uploader(
	"Upload your resume (PDF or DOCX)",
	type=["pdf", "docx"],
)
job_description = st.text_area(
	"Job description",
	height=300,
	placeholder="Paste the job description here...",
)

# Validate the inputs and show the milestone message.
if st.button("Analyze Resume"):
	if not resume_file and not job_description.strip():
		st.warning("Please upload a resume and enter a job description.")
	elif not resume_file:
		st.warning("Please upload a resume.")
	elif not job_description.strip():
		st.warning("Please enter a job description.")
	else:
		st.info("Analysis pipeline coming soon...")
