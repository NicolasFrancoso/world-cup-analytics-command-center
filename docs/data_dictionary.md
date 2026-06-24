# Data Dictionary

## World Cup Analytics Command Center

This document describes the datasets, tables and fields used in the **World Cup Analytics Command Center** project.

The purpose of this data dictionary is to make the project easier to understand, validate, maintain and reproduce.

---

## 1. Data Layers

The project follows a layered data structure:

| Layer     | Path              | Description                                              |
| --------- | ----------------- | -------------------------------------------------------- |
| Raw       | `data/raw/`       | Original data files collected from public sources        |
| Processed | `data/processed/` | Cleaned and standardized datasets                        |
| Gold      | `data/gold/`      | Analytical tables ready for reporting, KPIs and Power BI |

---

## 2. Raw Dataset: results.csv

Path:

```text
data/raw/results.csv
```

Description:

Raw dataset containing historical international football match results.

Granularity:

```text
One row per international football match
```

Expected columns:

| Column     | Type        | Description                                               |
| ---------- | ----------- | --------------------------------------------------------- |
| date       | date/string | Match date                                                |
| home_team  | string      | Team listed as home team                                  |
| away_team  | string      | Team listed as away team                                  |
| home_score | integer     | Goals scored by the home team                             |
| away_score | integer     | Goals scored by the away team                             |
| tournament | string      | Tournament name                                           |
| city       | string      | City where the match was played                           |
| country    | string      | Country where the match was played                        |
| neutral    | boolean     | Indicates whether the match was played in a neutral venue |

Notes:

* This file is used as the main source for the project.
* Only matches where `tournament = FIFA World Cup` are used in the main analytical layer.
* Additional datasets may be added in future versions.

---

## 3. Processed Dataset: world_cup_matches_processed.csv

Path:

```text
data/processed/world_cup_matches_processed.csv
```

Description:

Processed dataset containing only FIFA World Cup matches with additional analytical fields.

Granularity:

```text
One row per FIFA World Cup match
```

Columns:

| Column          | Type    | Description                                                         |
| --------------- | ------- | ------------------------------------------------------------------- |
| date            | date    | Match date converted to datetime format                             |
| home_team       | string  | Team listed as home team                                            |
| away_team       | string  | Team listed as away team                                            |
| home_score      | integer | Goals scored by the home team                                       |
| away_score      | integer | Goals scored by the away team                                       |
| tournament      | string  | Tournament name                                                     |
| city            | string  | City where the match was played                                     |
| country         | string  | Country where the match was played                                  |
| neutral         | boolean | Indicates whether the match was played in a neutral venue           |
| year            | integer | Year extracted from the match date                                  |
| month           | integer | Month extracted from the match date                                 |
| decade          | integer | Decade calculated from the match year                               |
| total_goals     | integer | Total goals scored in the match                                     |
| result          | string  | Match result from home/away perspective: Home Win, Away Win or Draw |
| home_points     | integer | Points earned by the home team                                      |
| away_points     | integer | Points earned by the away team                                      |
| goal_difference | integer | Home team goals minus away team goals                               |

---

## 4. Gold Table: fact_matches.csv

Path:

```text
data/gold/fact_matches.csv
```

Description:

Main match-level fact table used for reporting and dashboard development.

Granularity:

```text
One row per FIFA World Cup match
```

Columns:

| Column          | Type    | Description                                               |
| --------------- | ------- | --------------------------------------------------------- |
| date            | date    | Match date                                                |
| year            | integer | World Cup year                                            |
| month           | integer | Match month                                               |
| decade          | integer | Match decade                                              |
| home_team       | string  | Team listed as home team                                  |
| away_team       | string  | Team listed as away team                                  |
| home_score      | integer | Goals scored by the home team                             |
| away_score      | integer | Goals scored by the away team                             |
| tournament      | string  | Tournament name                                           |
| city            | string  | Match city                                                |
| country         | string  | Match country                                             |
| neutral         | boolean | Indicates whether the match was played in a neutral venue |
| total_goals     | integer | Total goals scored in the match                           |
| result          | string  | Match result from home/away perspective                   |
| home_points     | integer | Points earned by the home team                            |
| away_points     | integer | Points earned by the away team                            |
| goal_difference | integer | Home goals minus away goals                               |

Analytical use:

* Match-level KPIs
* Goals analysis
* Historical World Cup analysis
* Power BI fact table
* Match result analysis

---

## 5. Gold Table: team_performance.csv

Path:

```text
data/gold/team_performance.csv
```

Description:

Team-level analytical table with aggregated World Cup performance by year.

Granularity:

```text
One row per team per World Cup year
```

Columns:

| Column                  | Type    | Description                                                    |
| ----------------------- | ------- | -------------------------------------------------------------- |
| year                    | integer | World Cup year                                                 |
| team                    | string  | Team name                                                      |
| matches_played          | integer | Number of matches played by the team in that World Cup edition |
| wins                    | integer | Number of wins                                                 |
| draws                   | integer | Number of draws                                                |
| losses                  | integer | Number of losses                                               |
| goals_for               | integer | Total goals scored by the team                                 |
| goals_against           | integer | Total goals conceded by the team                               |
| points                  | integer | Total points based on the 3-1-0 points rule                    |
| goal_difference         | integer | Goals for minus goals against                                  |
| win_rate                | decimal | Wins divided by matches played                                 |
| goals_per_match         | decimal | Goals scored divided by matches played                         |
| goals_against_per_match | decimal | Goals conceded divided by matches played                       |

Analytical use:

* Team ranking
* Offensive performance analysis
* Defensive performance analysis
* Historical comparison by team
* Power BI team performance dashboard
* Inputs for future predictive modeling

---

## 6. Gold Table: world_cup_summary_by_year.csv

Path:

```text
data/gold/world_cup_summary_by_year.csv
```

Description:

World Cup edition-level summary table.

Granularity:

```text
One row per World Cup year
```

Columns:

| Column              | Type    | Description                                                 |
| ------------------- | ------- | ----------------------------------------------------------- |
| year                | integer | World Cup year                                              |
| matches             | integer | Total matches played in that edition                        |
| total_goals         | integer | Total goals scored in that edition                          |
| avg_goals_per_match | decimal | Average number of goals per match                           |
| host_countries      | integer | Number of distinct countries where matches were played      |
| cities              | integer | Number of distinct cities where matches were played         |
| teams               | integer | Number of participating teams based on available match data |

Analytical use:

* Historical World Cup evolution
* Goals trend analysis
* Match volume analysis
* Edition-level comparison
* Executive summary dashboard

---

## 7. Calculated Fields

This section summarizes the calculated fields created during the transformation process.

| Field                   | Formula / Rule                            | Description                      |
| ----------------------- | ----------------------------------------- | -------------------------------- |
| year                    | Extracted from `date`                     | Match year                       |
| month                   | Extracted from `date`                     | Match month                      |
| decade                  | `(year // 10) * 10`                       | Match decade                     |
| total_goals             | `home_score + away_score`                 | Total goals in the match         |
| result                  | Based on home and away scores             | Home Win, Away Win or Draw       |
| home_points             | 3 for win, 1 for draw, 0 for loss         | Points earned by home team       |
| away_points             | 3 for win, 1 for draw, 0 for loss         | Points earned by away team       |
| goal_difference         | `home_score - away_score` in fact table   | Home team goal difference        |
| team goal_difference    | `goals_for - goals_against` in team table | Team-level goal difference       |
| win_rate                | `wins / matches_played`                   | Team win rate                    |
| goals_per_match         | `goals_for / matches_played`              | Average goals scored per match   |
| goals_against_per_match | `goals_against / matches_played`          | Average goals conceded per match |

---

## 8. Current Data Model

Current analytical model:

```text
results.csv
   ↓
world_cup_matches_processed.csv
   ↓
fact_matches.csv
team_performance.csv
world_cup_summary_by_year.csv
```

Current model type:

```text
Simple analytical model with match-level, team-level and year-level tables
```

Future model type:

```text
Dimensional model with fact and dimension tables
```

---

## 9. Planned Future Tables

The following tables may be added in future versions:

| Table                      | Layer | Description                                                                        |
| -------------------------- | ----- | ---------------------------------------------------------------------------------- |
| dim_team.csv               | Gold  | Team dimension with continent, FIFA ranking, confederation and historical metadata |
| dim_date.csv               | Gold  | Calendar dimension for date-based analysis                                         |
| dim_group.csv              | Gold  | Group stage dimension                                                              |
| dim_competition_phase.csv  | Gold  | Competition phase dimension                                                        |
| fact_predictions.csv       | Gold  | Match prediction outputs                                                           |
| team_strength_index.csv    | Gold  | Team strength and ranking indicators                                               |
| group_difficulty.csv       | Gold  | Group difficulty analytical table                                                  |
| match_unpredictability.csv | Gold  | Match-level uncertainty and unpredictability score                                 |

---

## 10. Data Quality Considerations

Current data quality considerations:

* Team names may require standardization across historical periods.
* Tournament names must be validated before filtering.
* Some historical World Cup formats differ from modern formats.
* Host country logic may need adjustment for tournaments hosted by multiple countries.
* Draws in knockout stage may require additional penalty shootout data.
* Advanced match statistics are not available in the initial dataset.
* Future versions should include checks for duplicated matches, missing values and invalid scores.

---

## 11. Reproducibility

The datasets in the processed and gold layers are generated by running the main Python pipeline.

Main script:

```text
src/main.py
```

Command:

```bash
python src/main.py
```

Expected generated files:

```text
data/processed/world_cup_matches_processed.csv
data/gold/fact_matches.csv
data/gold/team_performance.csv
data/gold/world_cup_summary_by_year.csv
```

---

## 12. Change Log

| Date            | Change                                       |
| --------------- | -------------------------------------------- |
| Initial version | Created first version of the data dictionary |
