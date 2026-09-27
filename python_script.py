#### Importación paquetes y datos Python ####

# Importar paquete pandas como pd
import pandas as pd

# Importar paquete numpy como np
import numpy as np

# Importar conjunto datos formato CSV + asignar dataframe df_py_nba_rs_2526
df_py_nba_rs_2526 = pd.read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_regular_season_25_26_wide_data.csv")

#### Pipeline transformación datos Python (pandas) ####

# Detectar player_name con valores faltantes (NaN) en weight_kg (opcional)
df_py_nba_rs_2526.loc[df_py_nba_rs_2526['weight_kg'].isna(), 'player_name']

# Asignar dataframe original a nuevo dataframe transformado
df_py_nba_rs_2526_transformed = (df_py_nba_rs_2526

     # Completar valores faltantes (NaN) de variable weight_kg obtenidos de Wikipedia
    .assign(
        weight_kg=lambda df: df['weight_kg'].fillna(df['player_name'].map({
            "Chris Youngblood": 100.2, # https://en.wikipedia.org/wiki/Chris_Youngblood_(basketball)
            "Jahmyl Telfort": 99.8, # https://en.wikipedia.org/wiki/Jahmyl_Telfort
            "Jaylen Wells": 93.0, # https://en.wikipedia.org/wiki/Jaylen_Wells
            "LJ Cryer": 90.7, # https://en.wikipedia.org/wiki/LJ_Cryer
            "Lawson Lovering": 106.6, # https://en.wikipedia.org/wiki/Lawson_Lovering
            "Tolu Smith": 111.1 # https://en.wikipedia.org/wiki/Tolu_Smith
        }))
    )

    # Crear nuevas variables a partir de variables originales
    .assign(
      
        # Crear variable conference a partir de variable team
        conference=lambda df: np.select(
            [df['team'].isin(["ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DET", "IND",
                               "MIA", "MIL", "NYK", "ORL", "PHI", "TOR", "WAS"]),
             df['team'].isin(["DAL", "DEN", "GSW", "HOU", "LAC", "LAL", "MEM", "MIN",
                               "NOP", "OKC", "PHX", "POR", "SAC", "SAS", "UTA"])],
            ["Eastern", "Western"], default=None
        ),

        # Crear variable bmi_kgm2 a partir de variables weight_kg y height_m
        bmi_kgm2=lambda df: df['weight_kg'] / df['height_m'] ** 2,

        # Crear variable bmi_category a partir de variable bmi_kgm2
        bmi_category=lambda df: pd.cut(
            df['bmi_kgm2'], bins=[-np.inf, 18.5, 25, 30, 35, 40, np.inf],
            labels=["U", "N", "O", "OI", "OII", "OIII"], right=False
        ),

        # Crear variable usa_player a partir de variable country
        usa_player=lambda df: df['country'] == "USA",

        # Crear variable age_decimal_years a partir de fecha inicio temporada y variable birthdate
        age_decimal_years=lambda df: (pd.Timestamp("2025-10-21") - pd.to_datetime(df['birthdate'])).dt.days / 365.25,
        
        # Crear variable birth_year a partir de variable birthdate
        birth_year=lambda df: pd.to_datetime(df['birthdate']).dt.year,

        # Crear variable games_played a partir de variables wins y losses
        games_played=lambda df: df['wins'] + df['losses'],

        # Crear variable minutes_per_game a partir de variables minutes_played y games_played
        minutes_per_game=lambda df: np.where(df['games_played'] == 0, 0, df['minutes_played'] / df['games_played']),

        # Crear variable points a partir de variables one_point_made, two_point_made y three_point_made
        points=lambda df: df['one_point_made'] + df['two_point_made'] * 2 + df['three_point_made'] * 3,

        # Crear variable points_per_game a partir de variables points y games_played
        points_per_game=lambda df: np.where(df['games_played'] == 0, 0, df['points'] / df['games_played']),

        # Crear variable one_point_percentage a partir de variables one_point_made y one_point_attempted
        one_point_percentage=lambda df: np.where(
            df['one_point_attempted'] == 0, 0, df['one_point_made'] / df['one_point_attempted'] * 100
        ),

        # Crear variable two_point_percentage a partir de variables two_point_made y two_point_attempted
        two_point_percentage=lambda df: np.where(
            df['two_point_attempted'] == 0, 0, df['two_point_made'] / df['two_point_attempted'] * 100
        ),

        # Crear variable three_point_percentage a partir de variables three_point_made y three_point_attempted
        three_point_percentage=lambda df: np.where(
            df['three_point_attempted'] == 0, 0, df['three_point_made'] / df['three_point_attempted'] * 100
        ),

        # Crear variable field_goals_made a partir de variables two_point_made y three_point_made
        field_goals_made=lambda df: df['two_point_made'] + df['three_point_made'],

        # Crear variable field_goals_attempted a partir de variables two_point_attempted y three_point_attempted
        field_goals_attempted=lambda df: df['two_point_attempted'] + df['three_point_attempted'],

        # Crear variable field_goals_percentage a partir de variables field_goals_made y field_goals_attempted
        field_goals_percentage=lambda df: np.where(
            df['field_goals_attempted'] == 0, 0, df['field_goals_made'] / df['field_goals_attempted'] * 100
        ),

        # Crear variable effective_field_goals_percentage a partir de variables field_goals_made, three_point_made y field_goals_attempted
        effective_field_goals_percentage=lambda df: np.where(
            df['field_goals_attempted'] == 0, 0,
            (df['field_goals_made'] + 0.5 * df['three_point_made']) / df['field_goals_attempted'] * 100
        ),

        # Crear variable true_shooting_percentage a partir de variables points, field_goals_attempted y one_point_attempted
        true_shooting_percentage=lambda df: np.where(
            (df['field_goals_attempted'] + 0.44 * df['one_point_attempted']) == 0, 0,
            df['points'] / (2 * (df['field_goals_attempted'] + 0.44 * df['one_point_attempted'])) * 100
        ),

        # Crear variable rebounds a partir de variables offensive_rebounds y defensive_rebounds
        rebounds=lambda df: df['offensive_rebounds'] + df['defensive_rebounds'],

        # Crear variable rebounds_per_game a partir de variables rebounds y games_played
        rebounds_per_game=lambda df: np.where(df['games_played'] == 0, 0, df['rebounds'] / df['games_played']),

        # Crear variable assists_per_game a partir de variables assists y games_played
        assists_per_game=lambda df: np.where(df['games_played'] == 0, 0, df['assists'] / df['games_played']),

        # Crear variable turnovers_per_game a partir de variables turnovers y games_played
        turnovers_per_game=lambda df: np.where(df['games_played'] == 0, 0, df['turnovers'] / df['games_played']),

        # Crear variable steals_per_game a partir de variables steals y games_played
        steals_per_game=lambda df: np.where(df['games_played'] == 0, 0, df['steals'] / df['games_played']),

        # Crear variable blocks_per_game a partir de variables blocks y games_played
        blocks_per_game=lambda df: np.where(df['games_played'] == 0, 0, df['blocks'] / df['games_played']),

        # Crear variable personal_fouls_per_game a partir de variables personal_fouls y games_played
        personal_fouls_per_game=lambda df: np.where(df['games_played'] == 0, 0, df['personal_fouls'] / df['games_played']),

        # Crear variable fantasy_points a partir de variables points, rebounds, assists, steals, blocks y turnovers
        fantasy_points=lambda df: (
            df['points'] + df['rebounds'] * 1.2 + df['assists'] * 1.5
            + df['steals'] * 3 + df['blocks'] * 3 - df['turnovers']
        )
    )

    # Ordenar variables + eliminar variables no incluidas (season, season_type, player_id, age_completed_years, birthdate)
    .pipe(lambda df: df[[
        'player_name', 'team', 'conference', 'position', 
        'height_m', 'weight_kg', 'bmi_kgm2', 'bmi_category', 
        'country', 'usa_player', 
        'age_decimal_years', 'birth_year', 'experience', 
        'games_played', 'wins', 'losses', 
        'minutes_played', 'minutes_per_game',
        'points', 'points_per_game',
        'one_point_made', 'one_point_attempted', 'one_point_percentage',
        'two_point_made', 'two_point_attempted', 'two_point_percentage',
        'three_point_made', 'three_point_attempted', 'three_point_percentage',
        'field_goals_made', 'field_goals_attempted', 'field_goals_percentage',
        'effective_field_goals_percentage', 'true_shooting_percentage',
        'offensive_rebounds', 'defensive_rebounds', 'rebounds', 'rebounds_per_game',
        'assists', 'assists_per_game', 
        'turnovers', 'turnovers_per_game',
        'steals', 'steals_per_game', 
        'blocks', 'blocks_per_game',
        'personal_fouls', 'personal_fouls_per_game', 
        'fantasy_points'
    ]])

    # Convertir variables cualitativas nominales a tipo categórico no ordenado
    .astype({col: 'category' for col in ['player_name', 'team', 'conference', 'position', 'country']})

    # Convertir variable cualitativa ordinal a tipo categórico ordenado
    .astype({'bmi_category': pd.CategoricalDtype(categories=["U", "N", "O", "OI", "OII", "OIII"], ordered=True)})

    # Convertir variables cuantitativas discretas a tipo entero (números enteros)
    .astype({col: 'int64' for col in [
        'birth_year', 'experience', 'games_played', 'wins', 'losses', 'points',
        'one_point_made', 'one_point_attempted', 'two_point_made', 'two_point_attempted',
        'three_point_made', 'three_point_attempted', 'field_goals_made', 'field_goals_attempted',
        'offensive_rebounds', 'defensive_rebounds', 'rebounds', 'assists', 'turnovers', 'steals', 'blocks',
        'personal_fouls'
    ]})

    # Convertir variables cuantitativas continuas a tipo numérico (números decimales)
    .astype({col: 'float64' for col in [
        'height_m', 'weight_kg', 'bmi_kgm2', 'age_decimal_years',
        'minutes_played', 'minutes_per_game', 'points_per_game',
        'one_point_percentage', 'two_point_percentage', 'three_point_percentage',
        'field_goals_percentage', 'effective_field_goals_percentage', 'true_shooting_percentage',
        'rebounds_per_game', 'assists_per_game', 'turnovers_per_game', 'steals_per_game',
        'blocks_per_game', 'personal_fouls_per_game', 'fantasy_points'
    ]})

    # Etiquetar categorías variable position
    .assign(position=lambda df: df['position'].cat.rename_categories({
        "C": "Center", "C-F": "Center-Forward", "F": "Forward", "F-C": "Forward-Center",
        "F-G": "Forward-Guard", "G": "Guard", "G-F": "Guard-Forward"
    }))

    # Etiquetar categorías variable bmi_category
    .assign(bmi_category=lambda df: df['bmi_category'].cat.rename_categories({
        "U": "Underweight", "N": "Normal", "O": "Overweight",
        "OI": "Obese I", "OII": "Obese II", "OIII": "Obese III"
    }))
)

# Etiquetar variables (fuera del pipeline)
# NBA Stats Glossary: https://www.nba.com/stats/help/glossary
df_py_nba_rs_2526_transformed.attrs['column_labels'] = {
    'player_name': "Player Name", 
    'team': "Team", 
    'conference': "Conference",
    'position': "Position", 
    'height_m': "Height (m)", 
    'weight_kg': "Weight (kg)",
    'bmi_kgm2': "BMI (kg/m²)", 
    'bmi_category': "BMI Category", 
    'country': "Country",
    'usa_player': "USA Player", 
    'age_decimal_years': "Age (years)",
    'birth_year': "Birth Year",
    'experience': "Years of Experience", 
    'games_played': "Games Played (GP)",
    'wins': "Wins (W)", 
    'losses': "Losses (L)", 
    'minutes_played': "Minutes Played (MIN)",
    'minutes_per_game': "Minutes Per Game (MPG)", 
    'points': "Points (PTS)",
    'points_per_game': "Points Per Game (PPG)",
    'one_point_made': "Free Throws Made (FTM)", 
    'one_point_attempted': "Free Throws Attempted (FTA)",
    'one_point_percentage': "Free Throw Percentage (FT%)",
    'two_point_made': "2 Point Field Goals Made (2PM)", 
    'two_point_attempted': "2 Point Field Goals Attempted (2PA)",
    'two_point_percentage': "2 Point Field Goal Percentage (2P%)",
    'three_point_made': "3 Point Field Goals Made (3PM)", 
    'three_point_attempted': "3 Point Field Goals Attempted (3PA)",
    'three_point_percentage': "3 Point Field Goals Percentage (3P%)",
    'field_goals_made': "Field Goals Made (FGM)", 
    'field_goals_attempted': "Field Goals Attempted (FGA)",
    'field_goals_percentage': "Field Goal Percentage (FG%)",
    'effective_field_goals_percentage': "Effective Field Goal Percentage (eFG%)",
    'true_shooting_percentage': "True Shooting Percentage (TS%)",
    'offensive_rebounds': "Offensive Rebounds (OREB)", 
    'defensive_rebounds': "Defensive Rebounds (DREB)",
    'rebounds': "Rebounds (REB)", 
    'rebounds_per_game': "Rebounds Per Game (RPG)",
    'assists': "Assists (AST)", 
    'assists_per_game': "Assists Per Game (APG)",
    'turnovers': "Turnovers (TOV)", 
    'turnovers_per_game': "Turnovers Per Game (TOPG)",
    'steals': "Steals (STL)", 
    'steals_per_game': "Steals Per Game (SPG)",
    'blocks': "Blocks (BLK)", 
    'blocks_per_game': "Blocks Per Game (BPG)",
    'personal_fouls': "Personal Fouls (PF)", 
    'personal_fouls_per_game': "Personal Fouls Per Game (PFPG)",
    'fantasy_points': "Fantasy Points (FP)"
}
