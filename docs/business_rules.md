# Business Rules

## World Cup Analytics Command Center

This document describes the main business rules used in the **World Cup Analytics Command Center** project.

The goal of this documentation is to make the analytical logic clear, reproducible and easy to validate.

---

## 1. Data Source

The initial dataset used in this project is the international football results dataset.

The main raw file is:

```text
data/raw/results.csv
```

Expected columns:

| Column     | Description                                               |
| ---------- | --------------------------------------------------------- |
| date       | Match date                                                |
| home_team  | Team listed as home team                                  |
| away_team  | Team listed as away team                                  |
| home_score | Goals scored by the home team                             |
| away_score | Goals scored by the away team                             |
| tournament | Tournament name                                           |
| city       | City where the match was played                           |
| country    | Country where the match was played                        |
| neutral    | Indicates whether the match was played in a neutral venue |

---

## 2. World Cup Filter

Only matches where the tournament is equal to `FIFA World Cup` are considered for the main analytical layer.

Filtering rule:

```python
df["tournament"] == "FIFA World Cup"
```

This rule creates the processed World Cup dataset.

Output file:

```text
data/processed/world_cup_matches_processed.csv
```

---

## 3. Date Rules

The `date` column is converted to datetime format.

From this column, the following fields are created:

| Field  | Rule                            |
| ------ | ------------------------------- |
| year   | Year extracted from match date  |
| month  | Month extracted from match date |
| decade | Decade calculated from year     |

The decade is calculated as:

```python
decade = (year // 10) * 10
```

---

## 4. Match Result Rule

The match result is classified based on the final score.

| Condition                | Result   |
| ------------------------ | -------- |
| home_score > away_score  | Home Win |
| home_score < away_score  | Away Win |
| home_score == away_score | Draw     |

Created field:

```text
result
```

---

## 5. Points Rule

The standard football points system is used.

| Match outcome | Points |
| ------------- | ------ |
| Win           | 3      |
| Draw          | 1      |
| Loss          | 0      |

Created fields:

```text
home_points
away_points
```

Rules:

| Condition                | home_points | away_points |
| ------------------------ | ----------: | ----------: |
| home_score > away_score  |           3 |           0 |
| home_score < away_score  |           0 |           3 |
| home_score == away_score |           1 |           1 |

---

## 6. Goals Rule

Total goals are calculated as:

```text
total_goals = home_score + away_score
```

Goal difference is calculated from the home team perspective:

```text
goal_difference = home_score - away_score
```

Created fields:

```text
total_goals
goal_difference
```

---

## 7. Team Performance Rule

The team performance table converts match-level data into team-level data.

Each match generates two team records:

1. One record for the home team.
2. One record for the away team.

The following fields are calculated for each team and World Cup year:

| Field                   | Rule                           |
| ----------------------- | ------------------------------ |
| matches_played          | Count of matches played        |
| wins                    | Count of matches won           |
| draws                   | Count of matches drawn         |
| losses                  | Count of matches lost          |
| goals_for               | Total goals scored             |
| goals_against           | Total goals conceded           |
| points                  | Total points                   |
| goal_difference         | goals_for - goals_against      |
| win_rate                | wins / matches_played          |
| goals_per_match         | goals_for / matches_played     |
| goals_against_per_match | goals_against / matches_played |

Output file:

```text
data/gold/team_performance.csv
```

---

## 8. Yearly Summary Rule

The yearly summary table aggregates World Cup indicators by edition.

The following metrics are calculated:

| Metric              | Rule                                                               |
| ------------------- | ------------------------------------------------------------------ |
| matches             | Count of matches by year                                           |
| total_goals         | Sum of total goals                                                 |
| avg_goals_per_match | Average goals per match                                            |
| host_countries      | Number of distinct countries where matches were played             |
| cities              | Number of distinct cities where matches were played                |
| teams               | Maximum number between distinct home teams and distinct away teams |

Output file:

```text
data/gold/world_cup_summary_by_year.csv
```

---

## 9. Gold Layer Tables

The gold layer contains analytical tables ready for reporting and visualization.

Current gold tables:

| Table                         | Description                           |
| ----------------------------- | ------------------------------------- |
| fact_matches.csv              | Match-level fact table                |
| team_performance.csv          | Team-level performance table          |
| world_cup_summary_by_year.csv | World Cup edition-level summary table |

---

## 10. Fact Matches Table

The `fact_matches.csv` table contains one row per World Cup match.

Granularity:

```text
One row per World Cup match
```

Current fields:

| Field           | Description                                               |
| --------------- | --------------------------------------------------------- |
| date            | Match date                                                |
| year            | World Cup year                                            |
| month           | Match month                                               |
| decade          | Match decade                                              |
| home_team       | Team listed as home team                                  |
| away_team       | Team listed as away team                                  |
| home_score      | Goals scored by the home team                             |
| away_score      | Goals scored by the away team                             |
| tournament      | Tournament name                                           |
| city            | City where the match was played                           |
| country         | Country where the match was played                        |
| neutral         | Indicates whether the match was played in a neutral venue |
| total_goals     | Total goals scored in the match                           |
| result          | Match result from home/away perspective                   |
| home_points     | Points earned by the home team                            |
| away_points     | Points earned by the away team                            |
| goal_difference | Home goals minus away goals                               |

Output file:

```text
data/gold/fact_matches.csv
```

---

## 11. Important Notes

This project currently uses historical match results as the main source.

Some limitations may apply:

* The dataset may not contain advanced match statistics such as expected goals, shots, possession or player-level data.
* The current model does not yet separate group stage from knockout stage.
* Penalty shootout information may require an additional dataset.
* Host country interpretation may need adjustment for tournaments hosted by multiple countries.
* Future versions may include FIFA ranking, Elo rating and team strength indicators.
* Some historical matches may have naming inconsistencies depending on the original data source.
* Team names may require standardization in future versions.

---

## 12. Future Business Rules

Planned future rules include:

| Future Rule                                | Description                                                                 |
| ------------------------------------------ | --------------------------------------------------------------------------- |
| Group stage classification logic           | Calculate group standings based on points, goal difference and goals scored |
| Knockout stage qualification logic         | Identify teams advancing by stage                                           |
| Team strength index                        | Combine historical performance, ranking and recent form                     |
| Group difficulty score                     | Estimate how competitive each group is                                      |
| Match unpredictability score               | Identify matches with higher uncertainty                                    |
| Qualification probability                  | Estimate probability of each team advancing                                 |
| Overperformance and underperformance index | Compare expected performance against actual results                         |
| Penalty shootout rule                      | Include shootout results when knockout matches end in a draw                |
| Host advantage indicator                   | Measure potential performance differences for host nations                  |

---

## 13. Reproducibility

All business rules should be implemented in Python scripts inside the `src/` folder.

Main transformation file:

```text
src/transform.py
```

Main pipeline execution file:

```text
src/main.py
```

The pipeline can be executed from the project root using:

```bash
python src/main.py
```

Expected outputs:

```text
data/processed/world_cup_matches_processed.csv
data/gold/fact_matches.csv
data/gold/team_performance.csv
data/gold/world_cup_summary_by_year.csv
```

---

## 14. Change Log

| Date            | Change                                                |
| --------------- | ----------------------------------------------------- |
| Initial version | Created first version of business rules documentation |
