# Exploratory Data Analysis (EDA) Project

**Student project — Python, Pandas and Matplotlib**

## Objective
This project explores a student performance dataset to understand its basic patterns, compare subject scores, and check relationships between numeric columns.

## What it does
- Loads a CSV dataset with student scores, study hours, absences, gender, and course.
- Standardizes column names and trims extra spaces from text values.
- Checks for missing values and removes exact duplicate rows.
- Creates descriptive statistical summaries and a correlation matrix.
- Compares average scores by subject and course.
- Generates charts and a text report in the `output` folder.

## Tools used
- Python
- Pandas
- Matplotlib
- CSV dataset

## Project structure
```text
Exploratory_Data_Analysis_EDA_Project/
├── data/
│   └── student_performance.csv
├── output/
│   └── charts/
├── run.py
├── requirements.txt
├── .gitignore
└── README.md
```

The output files and charts are generated when the script is run.

## How to run
1. Install Python 3.10 or newer.
2. Open this project folder in VS Code.
3. Open the terminal in the project folder.
4. Install the required packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Run the analysis:

   ```powershell
   python run.py
   ```

If the `python` command does not work on Windows, use the full path to your Python executable instead.

## Output files
The script creates these files inside `output/`:
- `cleaned_data.csv`
- `statistical_summary.csv`
- `correlation_matrix.csv`
- `course_summary.csv`
- `report.txt`
- `charts/average_scores_by_subject.png`
- `charts/study_hours_vs_average_score.png`
- `charts/correlation_heatmap.png`

## Note
The included dataset is a small sample created for practice. The results are intended for learning exploratory data analysis, not for making decisions about real students. Correlation shows association and does not prove that one factor causes another.
