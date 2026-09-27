#### Instalación paquetes R ####

# Definir paquetes necesarios
  # reticulate: paquete para interoperabilidad entre R y Python
  # tidyverse: colección paquetes que incluye readr (importar datos), dplyr/tidyr (transformar datos) y ggplot2 (visualizar datos)
  # labelled: paquete para etiquetar variables
r_packages <- c("reticulate", "tidyverse", "labelled")

# Instalar conjuntamente paquetes necesarios si no instalados
install.packages(setdiff(r_packages, rownames(installed.packages())))

#### Importación paquetes y datos R ####

# Cargar conjuntamente paquetes necesarios
lapply(r_packages, library, character.only = TRUE)

# Importar conjunto datos formato CSV + asignar dataframe df_r_nba_rs_2526
df_r_nba_rs_2526 <- read_csv("https://raw.githubusercontent.com/EasySportsApps/nba_api_25_26_data/refs/heads/main/nba_players_regular_season_25_26_wide_data.csv")

#### Pipeline transformación datos R (dplyr) ####

# Detectar player_name con valores faltantes (NA) en weight_kg (opcional)
df_r_nba_rs_2526$player_name[is.na(df_r_nba_rs_2526$weight_kg)]

# Asignar dataframe original a nuevo dataframe transformado
df_r_nba_rs_2526_transformed <- df_r_nba_rs_2526 |> 
  
  # Completar valores faltantes (NA) de variable weight_kg obtenidos de Wikipedia
  mutate(
    weight_kg = case_when(
      player_name == "Chris Youngblood" ~ 100.2, # https://en.wikipedia.org/wiki/Chris_Youngblood_(basketball)
      player_name == "Jahmyl Telfort" ~ 99.8, # https://en.wikipedia.org/wiki/Jahmyl_Telfort
      player_name == "Jaylen Wells" ~ 93.0, # https://en.wikipedia.org/wiki/Jaylen_Wells
      player_name == "LJ Cryer" ~ 90.7, # https://en.wikipedia.org/wiki/LJ_Cryer
      player_name == "Lawson Lovering" ~ 106.6, # https://en.wikipedia.org/wiki/Lawson_Lovering
      player_name == "Tolu Smith" ~ 111.1, # https://en.wikipedia.org/wiki/Tolu_Smith
      TRUE ~ weight_kg)
  ) |>
  
  # Crear nuevas variables a partir de variables originales
  mutate( 
    
    # Crear variable conference a partir de variable team
    conference = case_when( 
      team %in% c("ATL", "BKN", "BOS", "CHA", "CHI", "CLE", "DET", "IND",
                  "MIA", "MIL", "NYK", "ORL", "PHI", "TOR", "WAS") ~ "Eastern",
      team %in% c("DAL", "DEN", "GSW", "HOU", "LAC", "LAL", "MEM", "MIN",
                  "NOP", "OKC", "PHX", "POR", "SAC", "SAS", "UTA") ~ "Western"),
    
    # Crear variable bmi_kgm2 a partir de variables weight_kg y height_m
    bmi_kgm2 = weight_kg / height_m^2,
    
    # Crear variable bmi_category a partir de variable bmi_kgm2
    bmi_category = case_when(
      bmi_kgm2 < 18.5 ~ "U",
      bmi_kgm2 < 25 ~ "N",
      bmi_kgm2 < 30 ~ "O",
      bmi_kgm2 < 35 ~ "OI",
      bmi_kgm2 < 40 ~ "OII",
      bmi_kgm2 >= 40 ~ "OIII"
    ),
    
    # Crear variable usa_player a partir de variable country
    usa_player = country == "USA",
    
    # Crear variable age_decimal_years a partir de fecha inicio temporada y variable birthdate
    age_decimal_years = (as.Date("2025-10-21") - birthdate) / 365.25,
    
    # Crear variable birth_year a partir de variable birthdate
    birth_year = format(birthdate, "%Y"),
    
    # Crear variable games_played a partir de variables wins y losses
    games_played = wins + losses,
    
    # Crear variable minutes_per_game a partir de variables minutes_played y games_played
    minutes_per_game = ifelse(games_played == 0, 0, minutes_played / games_played),
    
    # Crear variable points a partir de variables one_point_made, two_point_made y three_point_made
    points = one_point_made + (two_point_made * 2) + (three_point_made * 3),
    
    # Crear variable points_per_game a partir de variables points y games_played
    points_per_game = ifelse(games_played == 0, 0, points / games_played),
    
    # Crear variable one_point_percentage a partir de variables one_point_made y one_point_attempted
    one_point_percentage = ifelse(one_point_attempted == 0, 0, one_point_made / one_point_attempted * 100),
    
    # Crear variable two_point_percentage a partir de variables two_point_made y two_point_attempted
    two_point_percentage = ifelse(two_point_attempted == 0, 0, two_point_made / two_point_attempted * 100),
    
    # Crear variable three_point_percentage a partir de variables three_point_made y three_point_attempted
    three_point_percentage = ifelse(three_point_attempted == 0, 0, three_point_made / three_point_attempted * 100),
    
    # Crear variable field_goals_made a partir de variables two_point_made y three_point_made
    field_goals_made = two_point_made + three_point_made,
    
    # Crear variable field_goals_attempted a partir de variables two_point_attempted y three_point_attempted
    field_goals_attempted = two_point_attempted + three_point_attempted,
    
    # Crear variable field_goals_percentage a partir de variables field_goals_made y field_goals_attempted
    field_goals_percentage = ifelse(field_goals_attempted == 0, 0, field_goals_made / field_goals_attempted * 100),
    
    # Crear variable effective_field_goals_percentage a partir de variables field_goals_made, three_point_made y field_goals_attempted
    effective_field_goals_percentage = ifelse(field_goals_attempted == 0, 0, 
                                              (field_goals_made + 0.5 * three_point_made) / field_goals_attempted * 100),
    
    # Crear variable true_shooting_percentage a partir de variables points, field_goals_attempted y one_point_attempted
    true_shooting_percentage = ifelse((field_goals_attempted + 0.44 * one_point_attempted) == 0, 0,
                                      points / (2 * (field_goals_attempted + 0.44 * one_point_attempted)) * 100),
    
    # Crear variable rebounds a partir de variables offensive_rebounds y defensive_rebounds
    rebounds = offensive_rebounds + defensive_rebounds,
    
    # Crear variable rebounds_per_game a partir de variables rebounds y games_played
    rebounds_per_game = ifelse(games_played == 0, 0, rebounds / games_played),
    
    # Crear variable assists_per_game a partir de variables assists y games_played
    assists_per_game = ifelse(games_played == 0, 0, assists / games_played),
    
    # Crear variable turnovers_per_game a partir de variables turnovers y games_played
    turnovers_per_game = ifelse(games_played == 0, 0, turnovers / games_played),
    
    # Crear variable steals_per_game a partir de variables steals y games_played
    steals_per_game = ifelse(games_played == 0, 0, steals / games_played),
    
    # Crear variable blocks_per_game a partir de variables blocks y games_played
    blocks_per_game = ifelse(games_played == 0, 0, blocks / games_played),
    
    # Crear variable personal_fouls_per_game a partir de variables personal_fouls y games_played
    personal_fouls_per_game = ifelse(games_played == 0, 0, personal_fouls / games_played),
    
    # Crear variable fantasy_points a partir de variables points, rebounds, assists, steals, blocks y turnovers
    fantasy_points = points + (rebounds * 1.2) + (assists * 1.5) + (steals * 3) + (blocks * 3) - turnovers
    
  ) |> 
  
  # Ordenar variables + eliminar variables no incluidas (season, season_type, player_id, age_completed_years, birthdate)
  select(
    player_name, team, conference, position, 
    height_m, weight_kg, bmi_kgm2, bmi_category, 
    country, usa_player, 
    age_decimal_years, birth_year, experience, 
    games_played, wins, losses, 
    minutes_played, minutes_per_game,
    points, points_per_game,
    one_point_made, one_point_attempted, one_point_percentage,
    two_point_made, two_point_attempted, two_point_percentage,
    three_point_made, three_point_attempted, three_point_percentage,
    field_goals_made, field_goals_attempted, field_goals_percentage,
    effective_field_goals_percentage, true_shooting_percentage,
    offensive_rebounds, defensive_rebounds, rebounds, rebounds_per_game,
    assists, assists_per_game, 
    turnovers, turnovers_per_game,
    steals, steals_per_game, 
    blocks, blocks_per_game,
    personal_fouls, personal_fouls_per_game, 
    fantasy_points
  ) |>
  
  # Convertir variables cualitativas nominales a tipo categórico no ordenado
  mutate(across(c(player_name, team, conference, position, country), as.factor)) |>
  
  # Convertir variables cualitativas ordinales a tipo categórico ordenado
  mutate(
    bmi_category = factor(bmi_category,
                          levels = c("U", "N", "O", "OI", "OII", "OIII"),
                          ordered = TRUE)
  ) |>
  
  # Convertir variables cuantitativas discretas a tipo entero (números enteros)
  mutate(across(c(birth_year, experience, games_played, wins, losses, points,
                  one_point_made, one_point_attempted, two_point_made, two_point_attempted,
                  three_point_made, three_point_attempted, field_goals_made, field_goals_attempted,
                  offensive_rebounds, defensive_rebounds, rebounds, assists, turnovers, steals, blocks,
                  personal_fouls),
                as.integer)) |>
  
  # Convertir variables cuantitativas continuas a tipo numérico (números decimales)
  mutate(across(c(height_m, weight_kg, bmi_kgm2, age_decimal_years, 
                  minutes_played, minutes_per_game, points_per_game,
                  one_point_percentage, two_point_percentage, three_point_percentage,
                  field_goals_percentage, effective_field_goals_percentage, true_shooting_percentage,
                  rebounds_per_game, assists_per_game, turnovers_per_game, steals_per_game,
                  blocks_per_game, personal_fouls_per_game, fantasy_points),
                as.numeric)) |>
  
  # Etiquetar categorías variable position
  mutate(
    position = recode(position,
                      "C" = "Center",
                      "C-F" = "Center-Forward",
                      "F" = "Forward",
                      "F-C" = "Forward-Center",
                      "F-G" = "Forward-Guard",
                      "G" = "Guard",
                      "G-F" = "Guard-Forward")
  ) |>
  
  # Etiquetar categorías variable bmi_category
  mutate(
    bmi_category = recode(bmi_category,
                          "U" = "Underweight",
                          "N" = "Normal",
                          "O" = "Overweight",
                          "OI" = "Obese I",
                          "OII" = "Obese II",
                          "OIII" = "Obese III")
  ) |>
  
  # Etiquetar variables
  # NBA Stats Glossary: https://www.nba.com/stats/help/glossary
  set_variable_labels(
    player_name                       = "Player Name",
    team                              = "Team",
    conference                        = "Conference",
    position                          = "Position",
    height_m                          = "Height (m)",
    weight_kg                         = "Weight (kg)",
    bmi_kgm2                          = "BMI (kg/m²)",
    bmi_category                      = "BMI Category",
    country                           = "Country",
    usa_player                        = "USA Player",
    age_decimal_years                 = "Age (years)",
    birth_year                        = "Birth Year",
    experience                        = "Years of Experience",
    games_played                      = "Games Played (GP)",
    wins                              = "Wins (W)",
    losses                            = "Losses (L)",
    minutes_played                    = "Minutes Played (MIN)",
    minutes_per_game                  = "Minutes Per Game (MPG)",
    points                            = "Points (PTS)",
    points_per_game                   = "Points Per Game (PPG)",
    one_point_made                    = "Free Throws Made (FTM)",
    one_point_attempted               = "Free Throws Attempted (FTA)",
    one_point_percentage              = "Free Throw Percentage (FT%)",
    two_point_made                    = "2 Point Field Goals Made (2PM)",
    two_point_attempted               = "2 Point Field Goals Attempted (2PA)",
    two_point_percentage              = "2 Point Field Goal Percentage (2P%)",
    three_point_made                  = "3 Point Field Goals Made (3PM)",
    three_point_attempted             = "3 Point Field Goals Attempted (3PA)",
    three_point_percentage            = "3 Point Field Goals Percentage (3P%)",
    field_goals_made                  = "Field Goals Made (FGM)",
    field_goals_attempted             = "Field Goals Attempted (FGA)",
    field_goals_percentage            = "Field Goal Percentage (FG%)",
    effective_field_goals_percentage  = "Effective Field Goal Percentage (eFG%)",
    true_shooting_percentage          = "True Shooting Percentage (TS%)",
    offensive_rebounds                = "Offensive Rebounds (OREB)",
    defensive_rebounds                = "Defensive Rebounds (DREB)",
    rebounds                          = "Rebounds (REB)",
    rebounds_per_game                 = "Rebounds Per Game (RPG)",
    assists                           = "Assists (AST)",
    assists_per_game                  = "Assists Per Game (APG)",
    turnovers                         = "Turnovers (TOV)",
    turnovers_per_game                = "Turnovers Per Game (TOPG)",
    steals                            = "Steals (STL)",
    steals_per_game                   = "Steals Per Game (SPG)",
    blocks                            = "Blocks (BLK)",
    blocks_per_game                   = "Blocks Per Game (BPG)",
    personal_fouls                    = "Personal Fouls (PF)",
    personal_fouls_per_game           = "Personal Fouls Per Game (PFPG)",
    fantasy_points                    = "Fantasy Points (FP)"
  )

#### Instalación paquetes Python ####

# Definir paquetes necesarios
  # pandas: paquete para importar y transformar datos
  # numpy: paquete para operaciones numéricas
py_packages <- c("pandas", "numpy")

# Instalar conjuntamente paquetes necesarios si no instalados
if (!all(py_module_available(py_packages))) system2(py_config()$python, c("-m", "pip", "install", py_packages))
