# 🏀 NBA API 25-26 Data

[🇬🇧 English](README.md) | 🇪🇸 Español

Un par de scripts en Python para bajar datos de la NBA usando la API oficial (`stats.nba.com`, vía la librería `nba_api`) y dejarlos listos en CSV y Excel para analizar.

## 📦 Qué hay aquí

### 1. `nba_players_25_26_regular_season_wide_data`
Una fila por jugador de la **Temporada Regular 2025-26**.

- 🧍 **Datos de identidad:** temporada, equipo, posición (con las siglas oficiales de la NBA), id y nombre del jugador
- 📏 **Antropometría:** altura (m), peso (kg), país, edad, fecha de nacimiento y años de experiencia en la liga
- 📊 **Estadísticas de juego:** minutos jugados, victorias/derrotas, tiros por tipo (1, 2 y 3 puntos, anotados e intentados), rebotes, asistencias, pérdidas, robos, tapones y faltas

Altura y peso están en unidades métricas a propósito, para poder calcular el IMC u otros ratios sin tener que convertir nada en R o Python.

### 2. `nyk_players_25_26_playoffs_long_data`
Una fila por **jugador de los Knicks y partido de playoffs** (los 19 partidos de la postemporada 2025-26, desde la Primera Ronda hasta las Finales 🏆).

- Formato largo, pensado para ver la evolución partido a partido
- Incluye a todos los jugadores que aparecieron en algún momento, aunque no jugaran en un partido concreto
- Hay una columna `status` que dice si el jugador jugó o no, y si no jugó, por qué (decisión técnica, lesión, no viajó con el equipo, etc.)

## 📥 Cómo cargar los datos

No hace falta clonar el repositorio, puedes leer los CSV directamente desde GitHub.

**En R:**
```r
players <- read.csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_25_26_regular_season_wide_data.csv")
knicks_playoffs <- read.csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nyk_players_25_26_playoffs_long_data.csv")
```

**En Python:**
```python
import pandas as pd

players = pd.read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_25_26_regular_season_wide_data.csv")
knicks_playoffs = pd.read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nyk_players_25_26_playoffs_long_data.csv")
```

## 🔄 Regenerar los datos tú mismo (opcional)

Los CSV de este repo son una foto fija en el tiempo. Si quieres datos actualizados, puedes volver a ejecutar los scripts:

```bash
pip install nba_api pandas openpyxl
python nba_players_25_26_regular_season_wide_data.py
python nyk_players_25_26_playoffs_long_data.py
```

Ejecútalos desde tu propio ordenador, no desde Colab ni notebooks en la nube — la NBA bloquea la mayoría de esas IPs. La primera vez tarda unos minutos (los datos biográficos se piden jugador por jugador); las siguientes van rápido gracias al caché local.

## 📄 Licencia

Todavía no tiene licencia. Si quieres usar estos datos y necesitas que añada una, abre un issue y lo vemos.
