# 🧠 Job Description Analyzer & Internship Recommender

## 🚀 Overview

This project is an NLP-based application that analyzes the match between a user's skills and job descriptions, and also recommends relevant internships based on role and skill alignment.

It provides both **manual analysis** (user inputs JD + skills) and an **automated recommendation system** (user inputs role + skills).

---

## 🔍 Features

### 1. 📄 Job Description Analyzer

* Accepts **user skills + job description**
* Identifies:

  * ✅ Matching skills
  * ❌ Missing skills
  * 📊 Match percentage
  * 🔁 Skill frequency in the job description

---

### 2. 🤖 Internship Recommender (Automated)

* Accepts **user skills + desired role**
* Uses a **predefined dataset of internships**
* Provides:

  * 📊 Match percentage for each internship
  * 📌 Skill gap analysis (matched vs missing)
  * 💡 Recommendation (Apply / Not Apply)

---

### 3. 📊 Visualizations

* 🥧 Pie chart for **matched skills**
* 🥧 Pie chart for **unmatched skills**
* 📊 Bar chart comparing **match percentages across internships**

---

## 🛠️ Tech Stack

* **Language:** Python
* **Libraries:** Pandas, NumPy, Matplotlib / Seaborn, Scikit-learn
* **Concepts:** NLP, TF-IDF, Text Preprocessing, Skill Matching
* **Environment:** Jupyter Notebook / VS Code

---

## ⚙️ How It Works

### Job Description Analyzer

1. User inputs skills and job description
2. Text is preprocessed (cleaning, tokenization)
3. Skills are matched with extracted keywords
4. Match percentage and missing skills are calculated

---

### Internship Recommender

1. User inputs skills and target role
2. System filters relevant internships from dataset
3. Computes match percentage for each internship
4. Generates:

   * Skill gap analysis
   * Visual insights
   * Final recommendation

---

## 📈 Output

* Match percentage for job roles and internships
* List of matched and missing skills
* Visual insights (pie charts & bar graphs)
* Recommendation for each internship (Apply / Not Apply)

---

## 📁 Dataset

* Contains predefined internship listings with:

  * Role
  * Required skills
* Used for matching and recommendation

---

## 💡 Future Improvements

* Integrate real-time job data using APIs
* Add resume parsing for personalized recommendations
* Improve matching using advanced NLP models (BERT)
* Deploy as a web app using Streamlit

---

## 🎯 Conclusion

This project helps users evaluate their readiness for job roles and internships by providing clear insights into skill gaps, match percentages, and actionable recommendations.

It demonstrates practical application of **NLP, data analysis, and visualization** in solving real-world career guidance problems.
