# 🏀 NBA API 25-26 Data

🇬🇧 English | [🇪🇸 Español](README.es.md)

This repo has two NBA datasets (CSV) ready to use, plus the two Python scripts that generated them, in case you want to see exactly how the data was pulled or run it yourself to get fresh numbers.

## 📦 What's in this repo

| File | What it is |
|---|---|
| `nba_players_25_26_regular_season_wide_data.csv` | One row per player, 2025-26 Regular Season |
| `nyk_players_25_26_playoffs_long_data.csv` | One row per Knicks player per playoff game, 2025-26 postseason |
| `nba_players_25_26_regular_season_wide_data.py` | The script that generates the first CSV |
| `nyk_players_25_26_playoffs_long_data.py` | The script that generates the second CSV |

## 📊 The datasets

### `nba_players_25_26_regular_season_wide_data.csv`
One row per player for the 2025-26 Regular Season.

- 🧍 **Identity:** season, team, position (official NBA acronyms), player id and name
- 📏 **Anthropometrics:** height (m), weight (kg), country, age, birthdate, years of NBA experience
- 📊 **Game stats:** minutes played, wins/losses, shots by type (1, 2 and 3-point, made & attempted), rebounds, assists, turnovers, steals, blocks, fouls

Height and weight are in metric units on purpose, so you can calculate BMI or other ratios without converting anything.

### `nyk_players_25_26_playoffs_long_data.csv`
One row per Knicks player, per playoff game — all 19 games, First Round through the Finals 🏆.

- Long format, built for tracking game-by-game trends
- Includes every player who showed up at least once, even for games they didn't play
- A `status` column tells you whether the player actually played, and if not, why (coach's decision, injury, didn't travel with the team, etc.)

## 📥 Loading the data

You can read both CSVs straight from GitHub, no need to clone anything.

**In R:**
```r
df_nba_wide_data <- read.csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_25_26_regular_season_wide_data.csv")
df_nba_long_data <- read.csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nyk_players_25_26_playoffs_long_data.csv")
```

**In Python:**
```python
import pandas as pd

df_nba_wide_data = pd.read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_25_26_regular_season_wide_data.csv")
df_nba_long_data = pd.read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nyk_players_25_26_playoffs_long_data.csv")
```

## 🐍 About the scripts

The two `.py` files are the actual code used to build the CSVs above, pulling data straight from the NBA's official Stats API (`stats.nba.com`) via the [`nba_api`](https://github.com/swar/nba_api) library — no scraping, no third-party sources. They're here so anyone can check exactly where the numbers come from, and so you can rerun them yourself if you want a more recent snapshot than the one in this repo.

If you just want the data, you don't need to touch these at all — the CSVs above are enough.

If you do want to rerun them:

```bash
pip install nba_api pandas openpyxl
python nba_players_25_26_regular_season_wide_data.py
python nyk_players_25_26_playoffs_long_data.py
```

A few things worth knowing:
- Run them from your own machine, not Colab or similar — the NBA blocks most cloud provider IPs.
- The first run takes a few minutes, since bio data (height, birthdate, position...) is fetched player by player. It gets cached locally, so later runs are much faster.
- Each script also saves an `.xlsx` version with some basic formatting, on top of the CSV.

## ⚠️ About the data and how you can use it

This data comes from the NBA's official API (`stats.nba.com`) — it's not mine, I'm just collecting it and putting it here in a more convenient format. Its use is subject to the NBA's own terms and conditions, not mine.

The scripts (`.py`) themselves are mine, and you're free to use, copy, or adapt them however you like.
