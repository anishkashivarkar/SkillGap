import streamlit as st
import fitz
import spacy
from docx import Document
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------- NLP Model ----------
nlp = spacy.load("en_core_web_sm")


# ---------- Skill Vocabulary ----------
SKILLS = [
    "python",
    "java",
    "c++",
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "sql",
    "mysql",
    "pandas",
    "numpy",
    "scikit-learn",
    "tensorflow",
    "pytorch",
    "flask",
    "streamlit",
    "git",
    "github",
    "docker",
    "aws",
    "mongodb",
    "computer vision",
]


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

        document = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

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


# ---------- NLP Preprocessing ----------
def preprocess_text(text):

    doc = nlp(text)

    tokens = []

    for token in doc:

        if not token.is_stop and not token.is_punct and not token.is_space:
            tokens.append(token.lemma_.lower())

    return " ".join(tokens)


# ---------- Skill Extraction ----------
def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        if skill in text:
            found_skills.append(skill)

    return found_skills


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

        st.warning(
            "Please upload a resume and enter a job description."
        )

    elif not resume_file:

        st.warning("Please upload a resume.")

    elif not job_description.strip():

        st.warning("Please enter a job description.")

    else:

        try:

            # ---------- Extract Resume Text ----------
            resume_text = extract_resume_text(resume_file)

            if not resume_text.strip():

                st.error("Could not extract any text from the resume.")

            else:

                # ---------- Display Extracted Resume ----------
                st.subheader("Extracted Resume Text")

                st.text_area(
                    "Resume content",
                    resume_text,
                    height=400
                )


                # ---------- NLP Preprocessing ----------
                processed_resume = preprocess_text(resume_text)
                processed_job = preprocess_text(job_description)


                # ---------- Skill Extraction ----------
                resume_skills = extract_skills(processed_resume)
                job_skills = extract_skills(processed_job)


                # ---------- Skill Matching ----------
                matched_skills = list(
                    set(resume_skills) & set(job_skills)
                )

                missing_skills = list(
                    set(job_skills) - set(resume_skills)
                )


                # ---------- Skill Analysis ----------
                st.subheader("Skill Analysis")


                # Matched Skills
                st.write("### Matched Skills")

                if matched_skills:

                    st.success(
                        ", ".join(matched_skills)
                    )

                else:

                    st.info("No matching skills found.")


                # Missing Skills
                st.write("### Missing Skills")

                if missing_skills:

                    st.warning(
                        ", ".join(missing_skills)
                    )

                else:

                    st.success(
                        "No major missing skills found."
                    )


                # ---------- Skill Match Score ----------
                if job_skills:

                    skill_match_score = (
                        len(matched_skills) /
                        len(job_skills)
                    ) * 100

                else:

                    skill_match_score = 0


                st.metric(
                    "Skill Match",
                    f"{skill_match_score:.2f}%"
                )


                # ---------- TF-IDF ----------
                vectorizer = TfidfVectorizer()

                tfidf_matrix = vectorizer.fit_transform(
                    [
                        processed_resume,
                        processed_job
                    ]
                )


                # ---------- Cosine Similarity ----------
                similarity = cosine_similarity(
                    tfidf_matrix[0:1],
                    tfidf_matrix[1:2]
                )

                similarity_score = similarity[0][0] * 100


                # ---------- Similarity Score ----------
                st.subheader(
                    "Resume–Job Description Similarity"
                )

                st.metric(
                    "Similarity Score",
                    f"{similarity_score:.2f}%"
                )


                # ---------- Preprocessed Resume ----------
                st.subheader(
                    "Preprocessed Resume Text"
                )

                st.text_area(
                    "NLP processed resume",
                    processed_resume,
                    height=300
                )


                # ---------- Preprocessed Job Description ----------
                st.subheader(
                    "Preprocessed Job Description"
                )

                st.text_area(
                    "NLP processed job description",
                    processed_job,
                    height=300
                )


        except Exception as e:

            st.error(
                f"Error processing resume: {e}"
            )