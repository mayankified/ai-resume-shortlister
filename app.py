import streamlit as st
from utils.pdf_utils import extract_text_from_pdf
from utils.scoring_utils import score_resume

def skill_chips(skills, color="#2563eb"):
    if not skills:
        return "—"
    return " ".join(
        f"<span style='background:{color};color:white;padding:4px 8px;"
        f"border-radius:12px;font-size:12px;margin-right:4px;'>"
        f"{s}</span>"
        for s in skills
    )


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="NEED HRMS AI Resume Shortlisting",
    layout="wide",
)

hide_st_style = """
            <style>
            
            header {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.title("Need HRMS AI")
st.caption("AI-assisted candidate ranking based on job requirements")

# ================= JOB INPUT =================
st.markdown("## Job Requirements")

job_input_mode = st.radio(
    "Provide job requirements using",
    ["Text", "PDF", "Keywords"],
    horizontal=True
)

job_text = ""

if job_input_mode == "Text":
    job_text = st.text_area(
        "Job Description",
        height=180,
        placeholder="Paste job responsibilities, required skills, experience, etc."
    )

elif job_input_mode == "PDF":
    jd_file = st.file_uploader(
        "Upload Job Description (PDF)",
        type=["pdf"]
    )
    if jd_file:
        job_text = extract_text_from_pdf(jd_file)
        st.success("Job description extracted successfully")

elif job_input_mode == "Keywords":
    keywords = st.text_input(
        "Keywords",
        placeholder="React, Node.js, PostgreSQL, 2+ years experience"
    )
    if keywords:
        job_text = f"Required skills and qualifications: {keywords}"

# ================= RESUME UPLOAD =================
st.divider()
st.markdown("## 📄 Candidate Resumes")

uploaded_resumes = st.file_uploader(
    "Upload candidate resumes (PDF only)",
    type=["pdf"],
    accept_multiple_files=True
)

resume_texts = []

if uploaded_resumes:
    st.info(f"{len(uploaded_resumes)} resume(s) uploaded")
    for file in uploaded_resumes:
        resume_texts.append({
            "filename": file.name,
            "text": extract_text_from_pdf(file)
        })

# ================= SETTINGS =================
st.divider()
st.markdown("## ⚙️ Shortlisting Settings")

col1, col2 = st.columns(2)

with col1:
    shortlist_count = st.number_input(
        "Shortlist count",
        min_value=1,
        max_value=50,
        value=1
    )

with col2:
    waitlist_count = st.number_input(
        "Waitlist count",
        min_value=0,
        max_value=50,
        value=0
    )

# ================= RUN BUTTON =================
st.divider()
run = st.button("🚀 Run AI Shortlisting", use_container_width=True)

# ================= RESULTS =================
if run:
    if not job_text:
        st.error("Please provide job requirements")
    elif not resume_texts:
        st.error("Please upload at least one resume")
    else:
        results = []

        with st.spinner("Analyzing resumes with AI..."):
            for r in resume_texts:
                score_data = score_resume(job_text, r["text"])
                results.append({
                    "filename": r["filename"],
                    **score_data
                })

        results.sort(key=lambda x: x["score"], reverse=True)

        shortlisted = results[:shortlist_count]
        waitlisted = results[shortlist_count:shortlist_count + waitlist_count]
        rejected = results[shortlist_count + waitlist_count:]

        st.divider()
        st.markdown("## 🥇 Shortlisted Candidates")

        if shortlisted:
            for c in shortlisted:
                with st.container(border=True):
                    st.markdown(f"**📄 {c['filename']}**")
                    st.metric("Match Score", f"{c['score']} / 100")
                    st.write("✅ **Matched skills:**", ", ".join(c["matched_skills"]))
                    st.write("📝 **Reason:**", c["reason"])
        else:
            st.info("No shortlisted candidates")

        st.markdown("## 🥈 Waitlisted Candidates")
        if waitlisted:
            for c in waitlisted:
                with st.container(border=True):
                    st.markdown(f"**📄 {c['filename']}**")
                    st.metric("Match Score", f"{c['score']} / 100")
                    st.write("⚠️ **Missing skills:**", ", ".join(c["missing_skills"]))
                    st.write("📝 **Reason:**", c["reason"])
        else:
            st.info("No waitlisted candidates")

        st.markdown("## ❌ Rejected Candidates")
        if rejected:
            for c in rejected:
                with st.container(border=True):
                    st.markdown(f"**📄 {c['filename']}**")
                    st.metric("Match Score", f"{c['score']} / 100")
                    st.write("❌ **Missing skills:**", ", ".join(c["missing_skills"]))
        else:
            st.info("No rejected candidates")
