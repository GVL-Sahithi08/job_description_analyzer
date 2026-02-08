import streamlit as st
import re
from collections import Counter
import matplotlib.pyplot as plt
from train_model import run_job_recommender

from utils.skills import ROLE_SKILLS 
def load_css():
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()  

# -------------------- SIDEBAR NAVIGATION --------------------
st.sidebar.title("🔍 Navigation")

page = st.sidebar.radio(
    "Choose Analysis Mode",
    ["Manual Job Description Analyzer", "Automatic Job Recommendations"]
)

# ==================== MANUAL ANALYZER ====================
if page == "Manual Job Description Analyzer":

    # -------------------- PAGE CONFIG --------------------
    st.set_page_config(
        page_title="Job Description Analyzer",
        layout="wide"
    )

    # -------------------- LOAD CSS --------------------
    # -------------------- TITLE --------------------
    st.markdown("""
    <div class="section">
        <h1 class="custom-h1">📊 Job Description Analyzer</h1>
        <p>
        Rule-based NLP system to analyze job descriptions, calculate skill frequency,
        match percentage, and visualize insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # -------------------- INPUTS --------------------
    st.markdown('<div class="section">', unsafe_allow_html=True)
    jd_text = st.text_area("📄 Paste Job Description", height=160)
    candidate_input = st.text_input("👤 Candidate Skills (comma separated)")
    st.markdown('</div>', unsafe_allow_html=True)

    # Reset button
    col1, col2 = st.columns([6, 2])
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.clear()
            st.experimental_rerun()

    # -------------------- ANALYSIS --------------------
    if jd_text and candidate_input:

        text = jd_text.lower()
        candidate_skills = [s.strip().lower() for s in candidate_input.split(",")]

        # ---------- ROLE PREDICTION ----------
        role_scores = {}
        role_freq_map = {}

        for role, skills in ROLE_SKILLS.items():
            freq = Counter()
            for skill in skills:
                freq[skill] = len(re.findall(r"\b" + re.escape(skill) + r"\b", text))
            role_scores[role] = sum(freq.values())
            role_freq_map[role] = freq

        predicted_role = max(role_scores, key=role_scores.get)
        freq = role_freq_map[predicted_role]

        # ---------- MATCH / MISSING ----------
        matched_skills = {k: v for k, v in freq.items() if v > 0 and k in candidate_skills}
        missing_skills = {k: v for k, v in freq.items() if v > 0 and k not in candidate_skills}

        match_percentage = int((len(matched_skills) / len(ROLE_SKILLS[predicted_role])) * 100)

        # -------------------- TABS --------------------
        tab1, tab2, tab3 = st.tabs(["🏠 Home", "📊 Visualizations", "🧾 Preview"])

        # ==================== HOME TAB ====================
        with tab1:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown("<h2 class='custom-h2'>🔍 Analysis Results</h2>", unsafe_allow_html=True)
            st.write(f"**Predicted Role:** {predicted_role}")
            st.write(f"**Match Percentage:** {match_percentage}%")

            st.write("**✅ Matched Skills (with frequency):**")
            if matched_skills:
                for k, v in matched_skills.items():
                    st.write(f"- {k} → {v}")
            else:
                st.write("None")

            st.write("**❌ Missing Skills (with frequency):**")
            if missing_skills:
                for k, v in missing_skills.items():
                    st.write(f"- {k} → {v}")
            else:
                st.write("None")
            st.markdown('</div>', unsafe_allow_html=True)

        # ==================== VISUALS TAB ====================
        with tab2:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown("<h2 class='custom-h2'>📈 Skill Frequency Bar Chart</h2>", unsafe_allow_html=True)

            fig_bar, ax = plt.subplots(figsize=(10, 4))
            ax.bar(freq.keys(), freq.values())
            ax.set_xticklabels(freq.keys(), rotation=45, ha="right")
            ax.set_ylabel("Frequency")
            st.pyplot(fig_bar)

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("<h3 class='custom-h3'>✅ Matched Skills Distribution</h3>", unsafe_allow_html=True)
                if matched_skills:
                    fig1, ax1 = plt.subplots(figsize=(4, 4))
                    ax1.pie(matched_skills.values(),
                            labels=matched_skills.keys(),
                            autopct='%1.1f%%',
                            startangle=90)
                    ax1.axis("equal")
                    st.pyplot(fig1)
                else:
                    st.info("No matched skills")

            with col2:
                st.markdown("<h3 class='custom-h3'>❌ Missing Skills Distribution</h3>", unsafe_allow_html=True)
                if missing_skills:
                    fig2, ax2 = plt.subplots(figsize=(4, 4))
                    ax2.pie(missing_skills.values(),
                            labels=missing_skills.keys(),
                            autopct='%1.1f%%',
                            startangle=90)
                    ax2.axis("equal")
                    st.pyplot(fig2)
                else:
                    st.info("No missing skills")

            st.markdown('</div>', unsafe_allow_html=True)

        # ==================== PREVIEW TAB ====================
        with tab3:
            st.markdown('<div class="section">', unsafe_allow_html=True)
            st.markdown("<h2 class='custom-h2'>🧾 Summary Insight</h2>", unsafe_allow_html=True)

            if matched_skills:
                top_match = max(matched_skills, key=matched_skills.get)
                st.write(f"🔹 **Top Matching Skill:** {top_match}")

            if missing_skills:
                top_missing = max(missing_skills, key=missing_skills.get)
                st.write(f"🔸 **Top Missing Skill:** {top_missing}")

            st.write(
                f"The candidate matches **{match_percentage}%** of the required skills. "
                "Improving high-frequency missing skills will significantly boost suitability."
            )

            st.markdown('</div>', unsafe_allow_html=True)

    # -------------------- FOOTER --------------------
    st.markdown(
        """
        <div class="section">
            <h3 class="custom-h3">📸 Screenshots for Project Report</h3>
            <ul>
                <li>Home Page (Job Description Input)</li>
                <li>Skill Match Percentage</li>
                <li>Missing Skills Section</li>
                <li>Skill Frequency Chart</li>
            </ul>
            <p class="hint">
                Use these screenshots while preparing your final project report.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================== AUTOMATIC JOB RECOMMENDER ====================
elif page == "Automatic Job Recommendations":

    st.set_page_config(page_title="Job Recommendation Engine", layout="wide")

    st.markdown("""
    <div class="section">
        <h1 class="custom-h1">💼 Job Recommendation Engine</h1>
        <p>
        Enter your role and current skills to receive job recommendations,
        suitability percentage, missing skills, and visual insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # This runs your second version
    from train_model import run_job_recommender
    run_job_recommender()
