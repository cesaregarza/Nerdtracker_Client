from typing import TypedDict

NAME = "Name"
CONTROLLER = "Controller"
UNO_USERNAME = "unoUsername"
USERNAME = "username"
TIMES_PLAYED = "times_played"
LAST_PLAYED = "last_played"
KPM = "kpm"
KD_RATIO = "K/D Ratio"
KDR = "kdr"
KILLS = "Kills"
WIN_PERC = "Win %"
WINS = "Wins"
BEST_KILLSTREAK = "Best Killstreak"
LOSSES = "Losses"
TIES = "Ties"
CURR_WINSTREAK = "Current Win Streak"
DEATHS = "Deaths"
AVG_LIFESPAN = "Avg. Life"
ASSISTS = "Assists"
SCORE_PER_MIN = "Score/min"
SCORE_PER_GAME = "Score/game"
TOTAL_SCORE = "Score"
STAT_COLUMNS = [
    KD_RATIO,
    KILLS,
    WIN_PERC,
    WINS,
    BEST_KILLSTREAK,
    LOSSES,
    TIES,
    CURR_WINSTREAK,
    DEATHS,
    AVG_LIFESPAN,
    ASSISTS,
    SCORE_PER_MIN,
    SCORE_PER_GAME,
    TOTAL_SCORE,
]

FLOAT_COLUMNS = [
    KD_RATIO,
    KILLS,
    WIN_PERC,
    WINS,
    BEST_KILLSTREAK,
    LOSSES,
    TIES,
    CURR_WINSTREAK,
    DEATHS,
    ASSISTS,
    SCORE_PER_MIN,
    SCORE_PER_GAME,
    TOTAL_SCORE,
]
DISPLAY_COLUMNS = [
    NAME,
    CONTROLLER,
    UNO_USERNAME,
    USERNAME,
    TIMES_PLAYED,
    KDR,
    LAST_PLAYED,
    KPM,
    KD_RATIO,
    WIN_PERC,
    CURR_WINSTREAK,
]
REQUIRED_COLUMNS = [
    TIMES_PLAYED,
    KDR,
    LAST_PLAYED,
    KPM,
    "overall_" + KDR,
    "overall_" + KILLS,
    "overall_" + WIN_PERC,
    "overall_" + WINS,
    "overall_" + LOSSES,
    "overall_" + BEST_KILLSTREAK,
    "overall_" + TIES,
    "overall_" + CURR_WINSTREAK,
    "overall_" + AVG_LIFESPAN,
    "overall_" + ASSISTS,
    "overall_" + SCORE_PER_MIN,
    "overall_" + TOTAL_SCORE,
    "overall_" + SCORE_PER_GAME,
]


class StatColumns(TypedDict):
    KD_RATIO: float
    KILLS: int
    WIN_PERC: float
    WINS: int
    BEST_KILLSTREAK: int
    LOSSES: int
    TIES: int
    CURR_WINSTREAK: int
    DEATHS: int
    AVG_LIFESPAN: float
    ASSISTS: int
    SCORE_PER_MIN: float
    SCORE_PER_GAME: float
    TOTAL_SCORE: int
