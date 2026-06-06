# ============================================================
# Smart Label Quality Checker
# AI-Powered Data Quality Assessment Platform
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Custom modules
from src.duplicate import find_duplicates
from src.outliers import detect_outliers
from src.label_checker import check_label_consistency
from src.semantic_check import detect_semantic_duplicates, detect_mismatch
from src.report import generate_report
from src.pdf_report import create_pdf
from src.suggestions import generate_suggestions

st.set_page_config(
    page_title="Smart Label Quality Checker",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# Application Title
# ============================================================

st.title("🧠 Smart Label Quality Checker")

# ============================================================
# Dataset Upload Section
# Allows users to upload CSV datasets for analysis
# ============================================================

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:

    # ========================================================
    # Load Dataset
    # ========================================================

    df = pd.read_csv(uploaded_file)

    # ========================================================
    # Dataset Preview
    # Displays first few records for quick inspection
    # ========================================================

    st.write("## 📊 Dataset Preview")
    st.dataframe(df.head())

    # ========================================================
    # Duplicate Detection
    # Identifies exact duplicate records in the dataset
    # ========================================================

    st.write("## 🔴 Duplicate Entries")

    dup = find_duplicates(df)

    if len(dup) > 0:
        st.dataframe(dup)
    else:
        st.success("No duplicate entries found.")

    # ========================================================
    # Label Consistency Check
    # Detects inconsistent label formatting and naming
    # ========================================================

    st.write("## 🟡 Label Inconsistencies")

    label_issues = check_label_consistency(df, "label")

    if len(label_issues) > 0:
        st.dataframe(label_issues)
    else:
        st.success("No label inconsistencies found.")

    # ========================================================
    # Semantic Duplicate Detection
    # Uses embeddings and cosine similarity to identify
    # records with similar meanings
    # ========================================================

    st.write("## 🧠 Semantic Duplicates")

    semantic_duplicates = detect_semantic_duplicates(df, "text")

    if len(semantic_duplicates) > 0:
        st.dataframe(pd.DataFrame(semantic_duplicates))
    else:
        st.success("No semantic duplicates found.")

    # ========================================================
    # Mislabeled Data Detection
    # Flags semantically similar records having
    # different labels
    # ========================================================

    st.write("## 🚩 Possible Mislabeled Data")

    mismatches = detect_mismatch(
        df["text"].tolist(),
        df["label"].tolist()
    )

    if len(mismatches) > 0:
        st.dataframe(pd.DataFrame(mismatches))
    else:
        st.success("No label mismatches detected.")

    # ========================================================
    # Data Quality Score Calculation
    # Generates an overall dataset quality percentage
    # ========================================================

    duplicate_count = len(dup)
    label_count = len(label_issues)
    semantic_count = len(semantic_duplicates)
    mismatch_count = len(mismatches)
    outlier_count = 0

    total_issues = (
        duplicate_count
        + label_count
        + semantic_count
        + mismatch_count
        + outlier_count
    )

    total_rows = len(df)

    quality_score = round(
    max(
        0,
        100 - (
            total_issues / (total_rows * 5)
        ) * 100
    ),
    2
    )

    # ========================================================
    # Data Quality Dashboard
    # Displays key dataset quality metrics
    # ========================================================

    st.write("## 📈 Data Quality Dashboard")

    if quality_score >= 90:
        grade = "A+"
    elif quality_score >= 80:
        grade = "A"
    elif quality_score >= 70:
        grade = "B"
    elif quality_score >= 60:
        grade = "C"
    else:
        grade = "D"

    col1, col2, col3 = st.columns(3)

    col1.metric("Quality Score", f"{quality_score}%")
    col2.metric("Duplicates", duplicate_count)
    col3.metric("Label Issues", label_count)

    col4, col5, col6 = st.columns(3)

    col4.metric("Semantic Duplicates", semantic_count)
    col5.metric("Mislabeled", mismatch_count)
    col6.metric("Quality Grade", grade)

    # ========================================================
    # Dataset Health Status
    # Displays overall dataset condition
    # ========================================================

    if quality_score >= 90:
        st.success("🟢 Excellent Dataset Quality")
    elif quality_score >= 75:
        st.success("🟢 Good Dataset Quality")
    elif quality_score >= 50:
        st.warning("🟡 Moderate Dataset Quality")
    else:
        st.error("🔴 Poor Dataset Quality")

    # ========================================================
    # Issue Distribution Visualization
    # Pie chart showing issue breakdown
    # ========================================================

    st.write("## 📊 Issue Distribution")

    issue_data = {
        "Duplicates": duplicate_count,
        "Label Issues": label_count,
        "Semantic Duplicates": semantic_count
    }

    fig, ax = plt.subplots()

    ax.pie(
        issue_data.values(),
        labels=issue_data.keys(),
        autopct="%1.1f%%",
        wedgeprops={"edgecolor": "white", "linewidth": 2}
    )

    st.pyplot(fig)

    # ========================================================
    # Label Distribution Analysis
    # Displays frequency of each label category
    # ========================================================

    st.write("## 📊 Label Distribution")

    label_counts = df["label"].value_counts()

    fig2, ax2 = plt.subplots()

    ax2.bar(
        label_counts.index,
        label_counts.values
    )

    ax2.set_xlabel("Labels")
    ax2.set_ylabel("Count")
    ax2.set_title("Label Distribution")

    st.pyplot(fig2)

    # ========================================================
    # AI Auto-Fix Suggestions
    # Provides recommendations for improving dataset quality
    # ========================================================

    st.write("## 🤖 AI Auto-Fix Suggestions")

    suggestions = generate_suggestions(
        duplicate_count,
        label_count,
        semantic_count,
        mismatch_count
    )

    for suggestion in suggestions:
        st.info(suggestion)

    # ========================================================
    # Create cleaned dataset
    # Outlier Detection
    # Uses Isolation Forest to identify anomalous records
    # ======================================================== 

    cleaned_df = df.drop_duplicates()

    cleaned_df["label"] = (
        cleaned_df["label"]
        .str.strip()
        .str.lower()
    )

    st.write("## 🚨 Outlier Detection")

    if st.button("Run Outlier Detection"):

        result = detect_outliers(df, "text")

        if len(result) > 0:
            st.dataframe(result)
        else:
            st.success("No outliers detected.")

    # ========================================================
    # Cleaning Impact Analysis
    # Shows dataset improvement after cleaning
    # ========================================================

    st.write("## 📈 Cleaning Impact Analysis")

    original_records = len(df)
    clean_records = len(cleaned_df)

    removed_records = (
        original_records - clean_records
    )

    improvement = round(
        (removed_records / original_records) * 100,
        2
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Original Records", original_records)
    col2.metric("Clean Records", clean_records)
    col3.metric("Removed Records", removed_records)
    col4.metric("Improvement", f"{improvement}%")        

    # ========================================================
    # Clean Dataset Export
    # Removes duplicates and standardizes labels
    # ========================================================

    st.write("## 📥 Download Cleaned Dataset")

    st.download_button(
        label="Download Cleaned CSV",
        data=cleaned_df.to_csv(index=False),
        file_name="cleaned_dataset.csv",
        mime="text/csv"
    )

    # ========================================================
    # AI Data Quality Report
    # Generates a comprehensive dataset quality report
    # and allows users to download it in TXT and PDF formats.
    # ========================================================

    st.write("## 📄 AI Data Quality Report")

    report = generate_report(
        total_rows,
        quality_score,
        duplicate_count,
        label_count,
        semantic_count,
        mismatch_count
    )

    st.text_area(
        "Generated Report",
        report,
        height=300
    )

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="quality_report.txt",
        mime="text/plain"
    )

    # ========================================================
    # PDF Report Export
    # Converts the generated report into PDF format
    # for professional documentation and sharing.
    # ========================================================

    pdf_file = create_pdf(
    report,
    "quality_report.pdf"
    )

    with open(pdf_file, "rb") as file:
        st.download_button(
            label="📄 Download PDF Report",
            data=file,
            file_name="quality_report.pdf",
            mime="application/pdf"
        )