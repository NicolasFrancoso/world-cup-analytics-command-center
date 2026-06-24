# World Cup Analytics Command Center

End-to-end analytics project using Python, SQL and Power BI to transform World Cup data into executive dashboards, predictive insights and automated analytical pipelines.

## 1. Project Overview

The **World Cup Analytics Command Center** is an end-to-end data analytics project designed to monitor, analyze and forecast performance during the FIFA World Cup.

The project simulates a real business analytics environment where raw match, team and historical data are collected, processed, modeled and transformed into actionable insights for decision-makers.

The main goal is not only to analyze football results, but to demonstrate how a data analyst can build a complete analytical product combining:

* Data extraction and transformation
* Data modeling
* SQL-based analytical queries
* Python automation
* Forecasting and scenario simulation
* Power BI executive dashboards
* Business-oriented storytelling
* Documentation and reproducibility

## 2. Business Context

Large global events such as the World Cup generate a high volume of data and business opportunities for media companies, betting platforms, sponsors, retailers, tourism companies, sports analysts and digital products.

In this context, decision-makers may need to answer questions such as:

* Which teams are performing above or below expectations?
* Which groups are the most competitive?
* Which teams have the highest probability of advancing?
* Which matches are likely to be more unpredictable?
* How does current performance compare to historical strength?
* How can raw match data be converted into reliable executive indicators?

This project was built to answer these questions through a structured analytics solution.

## 3. Main Objectives

The main objectives of this project are:

1. Build an automated data pipeline for World Cup data.
2. Structure clean and reliable analytical datasets.
3. Create a dimensional data model for reporting and analysis.
4. Develop business KPIs related to team and match performance.
5. Build predictive models to estimate match outcomes and qualification probabilities.
6. Create an executive Power BI dashboard focused on decision-making.
7. Document the project structure, business rules and data logic.

## 4. Key Analytical Questions

This project aims to answer the following analytical questions:

* Which teams have the best overall performance?
* Which teams are the strongest offensively and defensively?
* Which groups are the most balanced or difficult?
* Which teams are overperforming or underperforming compared to expectations?
* What is the probability of each team advancing to the next stage?
* Which matches have the highest uncertainty?
* How do ranking, historical performance and current results relate to match outcomes?

## 5. Project Architecture

The project follows a layered analytics structure:

```text
Raw Data → Data Processing → Analytical Model → Forecasting → Power BI Dashboard
```

The proposed architecture includes:

* **Raw layer:** original data collected from public datasets or APIs.
* **Processed layer:** cleaned and standardized data.
* **Gold layer:** analytical tables ready for reporting and modeling.
* **SQL layer:** queries for KPIs and business analysis.
* **Python layer:** extraction, transformation, automation and modeling.
* **Power BI layer:** executive dashboard and storytelling.

## 6. Repository Structure

```text
world-cup-analytics-command-center/
│
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── gold/
│
├── notebooks/
│   └── 01_exploratory_analysis.ipynb
│
├── src/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── model.py
│
├── sql/
│   ├── create_tables.sql
│   └── kpi_queries.sql
│
├── powerbi/
│
├── docs/
│   ├── data_dictionary.md
│   └── business_rules.md
│
└── outputs/
```

## 7. Tools and Technologies

The project uses the following tools and technologies:

* **Python**: data extraction, cleaning, transformation and modeling
* **pandas**: data manipulation
* **NumPy**: numerical operations
* **SQL**: analytical queries and data modeling
* **Power BI**: dashboard development and data visualization
* **DAX**: business measures and KPIs
* **Power Query**: data preparation inside Power BI
* **Git and GitHub**: version control and project documentation

Possible future improvements:

* dbt Core for analytics engineering workflows
* DuckDB or PostgreSQL as analytical database
* GitHub Actions for pipeline automation
* Streamlit for interactive scenario simulation

## 8. Main KPIs

The dashboard and analytical model may include the following KPIs:

* Matches played
* Goals scored
* Goals conceded
* Goal difference
* Points by team
* Win rate
* Goals per match
* Offensive performance index
* Defensive performance index
* Group difficulty score
* Qualification probability
* Elimination risk
* Match unpredictability score
* Team performance ranking
* Overperformance and underperformance index

## 9. Data Model

The analytical model is designed using a dimensional approach.

Main fact tables:

* **Fact_Matches**
* **Fact_Group_Standings**
* **Fact_Team_Performance**
* **Fact_Predictions**

Main dimension tables:

* **Dim_Team**
* **Dim_Date**
* **Dim_Group**
* **Dim_Competition_Phase**
* **Dim_Stadium** *(optional)*

This structure allows scalable reporting and supports different analytical views, such as performance by team, group, date, phase and match.

## 10. Predictive Analytics

The predictive component of the project focuses on simple, interpretable and business-oriented models.

Possible modeling approaches include:

* Logistic Regression
* Random Forest
* Elo Rating
* Monte Carlo simulation
* Classification models for match outcomes
* Scenario simulation for group qualification

The goal is not only to predict results, but to create explainable insights that can support decision-making.

## 11. Power BI Dashboard

The Power BI dashboard is planned with the following pages:

### Executive Overview

High-level view of the competition, including total matches, goals, top teams, surprises and qualification outlook.

### Group Stage Analysis

Detailed analysis of group standings, points, goal difference, qualification probability and group difficulty.

### Team Performance

Team-level performance indicators, including offensive strength, defensive strength, efficiency and historical comparison.

### Match Intelligence

Match-level analysis with expected outcomes, uncertainty score and key performance indicators.

### Forecast and Scenario Simulation

Predictive view with qualification probabilities, projected standings and scenario analysis.

### Data Quality Monitoring

Monitoring page showing last update, processed records, missing data and pipeline consistency indicators.

## 12. Business Value

This project demonstrates how sports data can be transformed into a business analytics solution.

The same approach can be applied to different business contexts, such as:

* Sales performance monitoring
* Customer segmentation
* Revenue forecasting
* Operational performance
* Supply chain tracking
* Market intelligence
* Risk analysis
* Executive reporting

Although the project uses World Cup data, the underlying analytical logic is transferable to real business environments.

## 13. Expected Deliverables

The expected final deliverables are:

* Clean and structured datasets
* Python scripts for data processing
* SQL queries for analytical KPIs
* Exploratory analysis notebook
* Predictive model notebook or script
* Power BI dashboard
* Data dictionary
* Business rules documentation
* Final project summary

## 14. Project Status

Project in development.

Current stage:

* Repository created
* Initial folder structure defined
* README drafted
* Data sources under evaluation

Next steps:

1. Select and collect data sources.
2. Build the first raw datasets.
3. Create data cleaning and transformation scripts.
4. Define the analytical model.
5. Develop initial KPIs.
6. Build the first Power BI dashboard version.
7. Add predictive modeling and scenario simulation.

## 15. Author

**Nicolas Françoso**
Senior Data Analyst
Power BI | SQL | Python | Business Analytics | Automation | Data Visualization

This project is part of my professional portfolio, focused on demonstrating end-to-end analytics capabilities applied to a high-impact global event.
