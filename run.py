from pathlib import Path
import warnings

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "student_performance.csv"
OUTPUT_DIR = ROOT / "output"
CHART_DIR = OUTPUT_DIR / "charts"


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)
    rows_loaded = len(df)

    # Basic data checks and cleaning
    df.columns = df.columns.str.strip().str.lower()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].map(lambda value: value.strip() if isinstance(value, str) else value)
    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    missing_count = int(df.isna().sum().sum())

    # Descriptive statistics
    summary = df[numeric_cols].describe().round(2).T
    summary.to_csv(OUTPUT_DIR / "statistical_summary.csv", index_label="column")
    df.to_csv(OUTPUT_DIR / "cleaned_data.csv", index=False)

    # Correlation matrix
    corr = df[numeric_cols].corr().round(3)
    corr.to_csv(OUTPUT_DIR / "correlation_matrix.csv")

    # Course-level summary
    if "course" in df.columns and "math_score" in df.columns:
        course_summary = df.groupby("course")[["math_score", "reading_score", "writing_score"]].mean().round(2)
        course_summary.to_csv(OUTPUT_DIR / "course_summary.csv")

    # Chart 1: average scores by subject
    score_cols = [c for c in ["math_score", "reading_score", "writing_score"] if c in df.columns]
    if score_cols:
        df[score_cols].mean().plot(kind="bar", title="Average Student Scores by Subject", ylabel="Average score", rot=0)
        plt.tight_layout()
        plt.savefig(CHART_DIR / "average_scores_by_subject.png", dpi=150)
        plt.close()

    # Chart 2: study hours vs average score
    if "study_hours_per_day" in df.columns and score_cols:
        df["average_score"] = df[score_cols].mean(axis=1)
        plt.figure(figsize=(7, 5))
        plt.scatter(df["study_hours_per_day"], df["average_score"], alpha=0.8)
        plt.title("Study Hours vs Average Score")
        plt.xlabel("Study hours per day")
        plt.ylabel("Average score")
        plt.grid(True, alpha=0.25)
        plt.tight_layout()
        plt.savefig(CHART_DIR / "study_hours_vs_average_score.png", dpi=150)
        plt.close()

    # Chart 3: correlation heatmap without extra dependencies
    if not corr.empty:
        fig, ax = plt.subplots(figsize=(8, 6))
        image = ax.imshow(corr.values, cmap="coolwarm", vmin=-1, vmax=1)
        ax.set_xticks(range(len(corr.columns)))
        ax.set_yticks(range(len(corr.index)))
        ax.set_xticklabels(corr.columns, rotation=45, ha="right")
        ax.set_yticklabels(corr.index)
        ax.set_title("Correlation Matrix")
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
        fig.tight_layout()
        fig.savefig(CHART_DIR / "correlation_heatmap.png", dpi=150)
        plt.close(fig)

    # Build a concise text report
    report_lines = [
        "EXPLORATORY DATA ANALYSIS REPORT",
        "=" * 34,
        f"Rows loaded: {rows_loaded}",
        f"Rows after removing exact duplicates: {len(df)}",
        f"Exact duplicate rows removed: {duplicate_count}",
        f"Missing values found: {missing_count}",
        "",
        "NUMERIC COLUMN SUMMARY",
        "-" * 24,
        summary.to_string(),
        "",
        "AVERAGE SCORES BY SUBJECT",
        "-" * 25,
    ]
    if score_cols:
        report_lines.extend([f"{col}: {df[col].mean():.2f}" for col in score_cols])
    if "study_hours_per_day" in df.columns and score_cols:
        corr_value = df["study_hours_per_day"].corr(df[score_cols].mean(axis=1))
        report_lines.extend([
            "",
            f"Correlation between study hours and average score: {corr_value:.3f}",
            "Note: correlation describes association in this sample and does not prove causation."
        ])
    report_lines.extend([
        "",
        "Generated files:",
        "- cleaned_data.csv",
        "- statistical_summary.csv",
        "- correlation_matrix.csv",
        "- course_summary.csv (when course data is available)",
        "- charts/average_scores_by_subject.png",
        "- charts/study_hours_vs_average_score.png",
        "- charts/correlation_heatmap.png",
    ])
    (OUTPUT_DIR / "report.txt").write_text("\n".join(report_lines), encoding="utf-8")

    print("Exploratory Data Analysis completed successfully.")
    print(f"Rows loaded: {rows_loaded}; rows after duplicate removal: {len(df)}")
    print(f"Missing values found: {missing_count}")
    print(f"Output files saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
