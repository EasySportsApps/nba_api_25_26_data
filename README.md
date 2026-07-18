# 🏀 NBA API 25-26 Data

🇬🇧 English | [🇪🇸 Español](README.es.md)

Python scripts that pull NBA data straight from the official [`stats.nba.com`](https://www.nba.com/stats) API (via [`nba_api`](https://github.com/swar/nba_api)) and export clean, analysis-ready datasets in **CSV** and **Excel** format.

## 📦 What's inside

### 1. `nba_players_25_26_regular_season_wide_data`
One row per player for the **2025-26 Regular Season**.

- 🧍 **Identity:** season, team, position (official NBA acronyms), player id/name
- 📏 **Bio data:** height (m), weight (kg), country, age, birthdate, years of NBA experience
- 📊 **Game data:** minutes played, wins/losses, shooting splits by shot type (1-point / 2-point / 3-point, made & attempted), rebounds, assists, turnovers, steals, blocks, fouls

Height/weight in metric units, ready to calculate BMI or other anthropometric ratios directly in R or Python.

### 2. `nyk_players_25_26_playoffs_long_data`
One row per **New York Knicks player, per playoff game** (2025-26 postseason — all 19 games, First Round → NBA Finals 🏆).

- Long format: perfect for game-by-game trend analysis
- Includes **every player who appeared at least once**, across **every game** — even games they didn't play
- A `status` column flags whether the player actually played, or the specific reason they didn't (DNP - Coach's Decision, Injury/Illness, NWT - Not With Team, etc.)

## ⚙️ How it works

- Data is pulled directly from the NBA's official Stats API — no scraping, no third-party sources.
- Slow, stable data (bio info, birthdates, debut year) is **cached locally** after the first run, so re-running a script only re-fetches the stats that actually change game to game.
- Scripts must be run from a **local machine** (not cloud notebooks like Colab) — `stats.nba.com` blocks most cloud provider IPs.

## 🛠️ Requirements

```bash
pip install nba_api pandas openpyxl
```

## ▶️ Usage

```bash
python nba_players_25_26_regular_season_wide_data.py
python nyk_players_25_26_playoffs_long_data.py
```

First run may take a few minutes (per-player bio lookups); later runs are fast thanks to the cache.

## 📄 License

No license yet — feel free to open an issue if you'd like to use this data and need one added.
