# 🏀 NBA API 25-26 Data

[🇬🇧 English](README.md) | 🇪🇸 Español

Este repo tiene dos datasets de la NBA (CSV) listos para usar, más los dos scripts de Python con los que se generaron, por si te interesa ver cómo se sacaron los datos o quieres ejecutarlos tú mismo para tener números más recientes.

## 📦 Qué hay aquí

| Archivo | Qué es |
|---|---|
| `nba_players_25_26_regular_season_wide_data.csv` | Una fila por jugador, Temporada Regular 2025-26 |
| `nyk_players_25_26_playoffs_long_data.csv` | Una fila por jugador de los Knicks y partido de playoffs, postemporada 2025-26 |
| `nba_players_25_26_regular_season_wide_data.py` | El script que genera el primer CSV |
| `nyk_players_25_26_playoffs_long_data.py` | El script que genera el segundo CSV |

## 📊 Los datasets

### `nba_players_25_26_regular_season_wide_data.csv`
Una fila por jugador de la Temporada Regular 2025-26.

- 🧍 **Datos de identidad:** temporada, equipo, posición (siglas oficiales de la NBA), id y nombre del jugador
- 📏 **Antropometría:** altura (m), peso (kg), país, edad, fecha de nacimiento y años de experiencia en la liga
- 📊 **Estadísticas de juego:** minutos jugados, victorias/derrotas, tiros por tipo (1, 2 y 3 puntos, anotados e intentados), rebotes, asistencias, pérdidas, robos, tapones y faltas

Altura y peso están en unidades métricas a propósito, para poder calcular el IMC u otros ratios sin convertir nada.

### `nyk_players_25_26_playoffs_long_data.csv`
Una fila por jugador de los Knicks y partido de playoffs — los 19 partidos, desde la Primera Ronda hasta las Finales 🏆.

- Formato largo, pensado para ver la evolución partido a partido
- Incluye a todos los jugadores que aparecieron en algún momento, aunque no jugaran en un partido concreto
- Hay una columna `status` que dice si el jugador jugó o no, y si no jugó, por qué (decisión técnica, lesión, no viajó con el equipo, etc.)

## 📥 Cómo cargar los datos

Puedes leer los dos CSV directamente desde GitHub, sin clonar nada.

**En R:**
```r
df_nba_wide_data <- read.csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_25_26_regular_season_wide_data.csv")
df_nba_long_data <- read.csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nyk_players_25_26_playoffs_long_data.csv")
```

**En Python:**
```python
import pandas as pd

df_nba_wide_data = pd.read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_25_26_regular_season_wide_data.csv")
df_nba_long_data = pd.read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nyk_players_25_26_playoffs_long_data.csv")
```

## 🐍 Sobre los scripts

Los dos archivos `.py` son el código real con el que se construyeron los CSV de arriba, sacando los datos directamente de la API oficial de estadísticas de la NBA (`stats.nba.com`) a través de la librería [`nba_api`](https://github.com/swar/nba_api) — sin scraping, sin fuentes de terceros. Están aquí para que cualquiera pueda comprobar de dónde salen exactamente los números, y para que puedas volver a ejecutarlos si quieres una foto más reciente que la que hay en este repo.

Si solo quieres los datos, no necesitas tocar esto para nada — con los CSV de arriba te sobra.

Si quieres volver a ejecutarlos:

```bash
pip install nba_api pandas openpyxl
python nba_players_25_26_regular_season_wide_data.py
python nyk_players_25_26_playoffs_long_data.py
```

Cosas que conviene saber:
- Ejecútalos desde tu propio ordenador, no desde Colab ni similares — la NBA bloquea la mayoría de esas IPs.
- La primera ejecución tarda unos minutos, porque los datos biográficos (altura, fecha de nacimiento, posición...) se piden jugador por jugador. Se quedan guardados en un caché local, así que las siguientes veces va mucho más rápido.
- Cada script también guarda una versión en `.xlsx` con algo de formato, además del CSV.

## 📄 Licencia

Todavía no tiene licencia. Si quieres usar estos datos y necesitas que añada una, abre un issue y lo vemos.
