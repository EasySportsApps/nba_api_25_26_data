# 🏀 NBA API 25-26 Data

🇬🇧 English | [🇪🇸 Español](README.es.md)

A couple of Python scripts that pull NBA data straight from the official API (`stats.nba.com`, via the `nba_api` library) and export clean CSV/Excel datasets ready to analyze.

## 📦 What's in the repo

### 1. `nba_players_25_26_regular_season_wide_data`
One row per player for the **2025-26 Regular Season**.

- 🧍 **Identity:** season, team, position (official NBA acronyms), player id and name
- 📏 **Anthropometrics:** height (m), weight (kg), country, age, birthdate, years of NBA experience
- 📊 **Game stats:** minutes played, wins/losses, shots by type (1, 2 and 3-point, made & attempted), rebounds, assists, turnovers, steals, blocks, fouls

Height and weight are in metric units on purpose, so you can calculate BMI or other ratios without converting anything in R or Python.

### 2. `nyk_players_25_26_playoffs_long_data`
One row per **Knicks player, per playoff game** (all 19 games of the 2025-26 postseason, First Round through the Finals 🏆).

- Long format, built for tracking game-by-game trends
- Includes every player who showed up at least once, even for games they didn't play
- A `status` column tells you whether the player actually played, and if not, why (coach's decision, injury, didn't travel with the team, etc.)

## 📥 Loading the data

No need to clone the repo — you can read the CSVs straight from GitHub.

**In R:**
```r
players <- read.csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_25_26_regular_season_wide_data.csv")
knicks_playoffs <- read.csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nyk_players_25_26_playoffs_long_data.csv")
```

**In Python:**
```python
import pandas as pd

players = pd.read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_25_26_regular_season_wide_data.csv")
knicks_playoffs = pd.read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nyk_players_25_26_playoffs_long_data.csv")
```

## 🔄 Regenerating the data yourself (optional)

The CSVs in this repo are a snapshot. If you want up-to-date numbers, you can rerun the scripts yourself:

```bash
pip install nba_api pandas openpyxl
python nba_players_25_26_regular_season_wide_data.py
python nyk_players_25_26_playoffs_long_data.py
```

Run them from your own machine, not Colab or similar — the NBA blocks most cloud provider IPs. The first run takes a few minutes (bio data is fetched player by player); later runs are fast thanks to the local cache.

## 📄 License

No license yet — open an issue if you'd like to use this data and need one added.
