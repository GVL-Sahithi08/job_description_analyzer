import streamlit as st
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

def run_job_recommender():

    st.write("Enter your role and current skills to get recommended jobs and suitability analysis.")

    # --- Role options ---
    roles = {
        "Data Analyst": "data/data_analyst_jobs.csv",
        "Data Scientist": "data/data_scientist_jobs.csv",
        "Data Engineer": "data/data_engineer_jobs.csv",
        "Software Engineer": "data/software_engineer_jobs.csv"
    }

    # --- User Inputs ---
    role_input = st.selectbox("Select your desired role:", list(roles.keys()))
    skills_input = st.text_input("Enter your current skills (comma-separated):")

    if st.button("Get Job Recommendations"):

        if not skills_input.strip():
            st.warning("Please enter your skills to get recommendations.")
            return

        user_skills = [skill.strip().lower() for skill in skills_input.split(",")]
        df = pd.read_csv(roles[role_input])

        results = []
        all_matching_skills = []
        all_missing_skills = []

        for _, row in df.iterrows():
            job_skills = [s.strip().lower() for s in row["Required Skills"].split(",")]
            matching = list(set(user_skills) & set(job_skills))
            missing = list(set(job_skills) - set(user_skills))
            match_percent = round(len(matching) / len(job_skills) * 100, 2)

            results.append({
                "Job Role": row["Job Role"],
                "Company": row["Company"],
                "Job Description": row["Job Description"],
                "Link": row["Link"],
                "Matching Skills": matching,
                "Missing Skills": missing,
                "Suitability (%)": match_percent
            })

            all_matching_skills.extend(matching)
            all_missing_skills.extend(missing)

        results = sorted(results, key=lambda x: x["Suitability (%)"], reverse=True)

        # --- Display Results ---
        st.subheader(f"Recommended Jobs for {role_input}")

        for job in results:
            st.markdown(f"""
            <div class="card">
                <h3>{job['Job Role']} - {job['Company']}</h3>
                <p>{job['Job Description']}</p>
                <p><strong>Matching Skills:</strong> {', '.join(job['Matching Skills'])}</p>
                <p><strong>Missing Skills:</strong> {', '.join(job['Missing Skills'])}</p>
                <p><strong>Suitability:</strong> {job['Suitability (%)']}%</p>
                <a href="{job['Link']}" target="_blank">Apply Here</a>
            </div>
            """, unsafe_allow_html=True)

            # --- Pie charts (split into two columns) ---
            col1, col2 = st.columns(2)

            # -------- MATCHING PIE --------
            with col1:
                st.markdown("### ✅ Matching Skills")
                if job["Matching Skills"]:
                    fig1, ax1 = plt.subplots(figsize=(3.5, 3.5))
                    counts = Counter(job["Matching Skills"])

                    ax1.pie(
                        counts.values(),
                        labels=counts.keys(),
                        autopct="%1.1f%%",
                        startangle=90
                    )
                    ax1.axis("equal")
                    st.pyplot(fig1)
                else:
                    st.info("No matching skills")

            # -------- MISSING PIE --------
            with col2:
                st.markdown("### ❌ Missing Skills")
                if job["Missing Skills"]:
                    fig2, ax2 = plt.subplots(figsize=(3.5, 3.5))
                    counts = Counter(job["Missing Skills"])

                    ax2.pie(
                        counts.values(),
                        labels=counts.keys(),
                        autopct="%1.1f%%",
                        startangle=90
                    )
                    ax2.axis("equal")
                    st.pyplot(fig2)
                else:
                    st.success("No missing skills 🎯")

            # --- Static suggestions per job ---
            if len(job["Missing Skills"]) == 0:
                st.success("You are fully qualified for this role!")
            elif len(job["Missing Skills"]) <= 2:
                st.info("Good match! Learn the missing skills to improve chances.")
            else:
                st.warning("Skill gap is high. Upskilling recommended before applying.")

        # --- Overall Summary ---
        if all_missing_skills:
            st.write(
                "**Most frequently missing skill:**",
                Counter(all_missing_skills).most_common(1)[0][0]
            )

        if all_matching_skills:
            st.write(
                "**Most frequently matching skill:**",
                Counter(all_matching_skills).most_common(1)[0][0]
            )

        # --- Overall Suitability Bar Chart ---
        job_titles = [job["Job Role"] + " @ " + job["Company"] for job in results]
        match_percentages = [job["Suitability (%)"] for job in results]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.barh(job_titles, match_percentages, color="#00c8ff")
        ax.set_xlabel("Suitability %")
        ax.set_ylabel("Job Role")
        ax.set_title("Overall Suitability Percentage for Recommended Jobs")
        ax.invert_yaxis()

        st.pyplot(fig)
