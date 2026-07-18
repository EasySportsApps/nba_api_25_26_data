# 🏀 NBA API 25-26 Data

[🇬🇧 English](README.md) | 🇪🇸 Español

Scripts en Python que descargan datos de la NBA directamente desde la API oficial [`stats.nba.com`](https://www.nba.com/stats) (a través de [`nba_api`](https://github.com/swar/nba_api)) y exportan datasets limpios y listos para analizar en formato **CSV** y **Excel**.

## 📦 Qué incluye

### 1. `nba_players_25_26_regular_season_wide_data`
Una fila por jugador para la **Temporada Regular 2025-26**.

- 🧍 **Identidad:** temporada, equipo, posición (acrónimos oficiales de la NBA), id/nombre del jugador
- 📏 **Datos biográficos:** altura (m), peso (kg), país, edad, fecha de nacimiento, años de experiencia en la NBA
- 📊 **Datos de juego:** minutos jugados, victorias/derrotas, desglose de tiros por tipo (1 punto / 2 puntos / 3 puntos, anotados e intentados), rebotes, asistencias, pérdidas, robos, tapones, faltas

Altura y peso en unidades métricas, listos para calcular el IMC u otros ratios antropométricos directamente en R o Python.

### 2. `nyk_players_25_26_playoffs_long_data`
Una fila por **jugador de los New York Knicks, por partido de playoffs** (postemporada 2025-26 — los 19 partidos, desde la Primera Ronda hasta las Finales de la NBA 🏆).

- Formato largo: perfecto para analizar tendencias partido a partido
- Incluye a **todos los jugadores que aparecieron al menos una vez**, en **todos los partidos** — incluso en los que no jugaron
- Una columna `status` indica si el jugador realmente jugó, o el motivo específico por el que no lo hizo (DNP - Coach's Decision, Injury/Illness, NWT - Not With Team, etc.)

## ⚙️ Cómo funciona

- Los datos se obtienen directamente de la API oficial de estadísticas de la NBA — sin scraping, sin fuentes de terceros.
- Los datos lentos y estables (información biográfica, fechas de nacimiento, año de debut) se **guardan en caché localmente** tras la primera ejecución, así que volver a ejecutar un script solo actualiza las estadísticas que realmente cambian de partido en partido.
- Los scripts deben ejecutarse desde un **ordenador local** (no en notebooks en la nube como Colab) — `stats.nba.com` bloquea la mayoría de IPs de proveedores en la nube.

## 🛠️ Requisitos

```bash
pip install nba_api pandas openpyxl
```

## ▶️ Uso

```bash
python nba_players_25_26_regular_season_wide_data.py
python nyk_players_25_26_playoffs_long_data.py
```

La primera ejecución puede tardar varios minutos (consultas biográficas por jugador); las siguientes son rápidas gracias a la caché.

## 📄 Licencia

Todavía sin licencia — si quieres usar estos datos y necesitas que se añada una, abre un issue sin problema.
