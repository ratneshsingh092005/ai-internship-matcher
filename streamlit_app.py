import os
import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")
st.set_page_config(page_title="AI Internship Matcher", page_icon="🎓", layout="wide")
st.title("🎓 AI Internship Matcher")
st.caption("Semantic resume matching with skill-gap and opportunity-quality analysis")

uploaded = st.file_uploader("Upload your resume", type=["pdf"])
if uploaded and st.button("Analyze & Find Internships", type="primary"):
    with st.spinner("Analyzing resume and finding relevant internships..."):
        response = requests.post(f"{API_URL}/analyze-resume", files={"file": (uploaded.name, uploaded.getvalue(), "application/pdf")}, timeout=120)
    if response.ok:
        analysis = response.json()
        st.subheader("Detected Skills")
        st.write(" · ".join(analysis["skills"]) or "No configured skills detected")
        # Reuse extracted text through a lightweight local extraction call to API is intentionally avoided;
        # FastAPI's primary recommendation endpoint accepts text, so the dashboard extracts the PDF locally.
        import fitz
        text = " ".join(page.get_text("text") for page in fitz.open(stream=uploaded.getvalue(), filetype="pdf"))
        rec = requests.post(f"{API_URL}/recommendations", json={"resume_text": text, "top_k": 10}, timeout=120)
        if not rec.ok:
            st.error(rec.text)
        else:
            for item in rec.json()["recommendations"]:
                with st.container(border=True):
                    st.subheader(item["title"])
                    st.write(f"**{item['company']}** · {item['location']} · {'Remote' if item['remote'] else 'On-site'}")
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Match", f"{item['final_score']:.1f}%")
                    c2.metric("Skills", f"{item['skill_match_score']:.1f}%")
                    c3.metric("Quality", f"{item['quality_score']}/100")
                    st.write("**Matched:** " + (", ".join(item["matched_skills"]) or "None"))
                    st.write("**Missing:** " + (", ".join(item["missing_skills"]) or "None"))
                    if item["warnings"]:
                        st.warning("; ".join(item["warnings"]))
                    if item["application_url"]:
                        st.link_button("View Application", item["application_url"])
    else:
        st.error(response.text)

st.divider()
st.caption("Semantic scores represent similarity, not probability of selection. Quality warnings are heuristic signals, not proof of fraud.")
