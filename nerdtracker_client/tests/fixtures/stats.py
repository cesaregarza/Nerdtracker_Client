import pytest

import nerdtracker_client.constants.stats as ntc_stats


@pytest.fixture
def fake_stats() -> ntc_stats.StatColumns:
    stat_dict = {
        ntc_stats.KD_RATIO: "1.00",
        ntc_stats.WIN_PERC: "50.0%",
        ntc_stats.SCORE_PER_MIN: "100.00",
        ntc_stats.KILLS: "100",
        ntc_stats.DEATHS: "100",
        ntc_stats.WINS: "100",
        ntc_stats.LOSSES: "100",
        ntc_stats.TIES: "1",
        ntc_stats.ASSISTS: "100",
        ntc_stats.BEST_KILLSTREAK: "5",
        ntc_stats.AVG_LIFESPAN: "15.0s",
        ntc_stats.TOTAL_SCORE: "100,000",
    }
    return ntc_stats.StatColumns(**stat_dict)  # type: ignore


@pytest.fixture
def joy_stats() -> ntc_stats.StatColumns:
    stat_dict = {
        ntc_stats.KD_RATIO: "1.79",
        ntc_stats.WIN_PERC: "52.9%",
        ntc_stats.SCORE_PER_MIN: "742.72",
        ntc_stats.KILLS: "52,349",
        ntc_stats.DEATHS: "29,297",
        ntc_stats.WINS: "793",
        ntc_stats.LOSSES: "535",
        ntc_stats.TIES: "8",
        ntc_stats.ASSISTS: "3,252",
        ntc_stats.BEST_KILLSTREAK: "31",
        ntc_stats.AVG_LIFESPAN: "27.5s",
        ntc_stats.TOTAL_SCORE: "9,973,255",
    }
    return ntc_stats.StatColumns(**stat_dict)  # type: ignore


@pytest.fixture
def askinner_stats() -> ntc_stats.StatColumns:
    stat_dict = {
        ntc_stats.KD_RATIO: "1.35",
        ntc_stats.WIN_PERC: "78.0%",
        ntc_stats.SCORE_PER_MIN: "445.12",
        ntc_stats.KILLS: "1,392",
        ntc_stats.DEATHS: "1,028",
        ntc_stats.WINS: "46",
        ntc_stats.LOSSES: "12",
        ntc_stats.TIES: "0",
        ntc_stats.ASSISTS: "115",
        ntc_stats.BEST_KILLSTREAK: "12",
        ntc_stats.AVG_LIFESPAN: "32.773s",
        ntc_stats.TOTAL_SCORE: "249,940",
    }
    return ntc_stats.StatColumns(**stat_dict)  # type: ignore


@pytest.fixture
def unwitty_stats() -> ntc_stats.StatColumns:
    stat_dict = {
        ntc_stats.KD_RATIO: "1.44",
        ntc_stats.WIN_PERC: "67.7%",
        ntc_stats.SCORE_PER_MIN: "510.42",
        ntc_stats.KILLS: "932",
        ntc_stats.DEATHS: "646",
        ntc_stats.WINS: "23",
        ntc_stats.LOSSES: "11",
        ntc_stats.TIES: "0",
        ntc_stats.ASSISTS: "53",
        ntc_stats.BEST_KILLSTREAK: "19",
        ntc_stats.AVG_LIFESPAN: "33.029s",
        ntc_stats.TOTAL_SCORE: "181,515",
    }
    return ntc_stats.StatColumns(**stat_dict)  # type: ignore


@pytest.fixture
def clicky_stats() -> ntc_stats.StatColumns:
    stats_dict = {
        ntc_stats.KD_RATIO: "0.91",
        ntc_stats.WIN_PERC: "53.8%",
        ntc_stats.SCORE_PER_MIN: "311.84",
        ntc_stats.KILLS: "3,941",
        ntc_stats.DEATHS: "4,318",
        ntc_stats.WINS: "120",
        ntc_stats.LOSSES: "80",
        ntc_stats.TIES: "0",
        ntc_stats.ASSISTS: "1,111",
        ntc_stats.BEST_KILLSTREAK: "10",
        ntc_stats.AVG_LIFESPAN: "26.556s",
        ntc_stats.TOTAL_SCORE: "595,980",
    }
    return ntc_stats.StatColumns(**stats_dict)  # type: ignore


@pytest.fixture
def cali_stats() -> ntc_stats.StatColumns:
    stats_dict = {
        ntc_stats.KD_RATIO: "1.41",
        ntc_stats.WIN_PERC: "79.0%",
        ntc_stats.SCORE_PER_MIN: "396.54",
        ntc_stats.KILLS: "1,571",
        ntc_stats.DEATHS: "1,111",
        ntc_stats.WINS: "45",
        ntc_stats.LOSSES: "11",
        ntc_stats.TIES: "0",
        ntc_stats.ASSISTS: "36",
        ntc_stats.BEST_KILLSTREAK: "12",
        ntc_stats.AVG_LIFESPAN: "31.495s",
        ntc_stats.TOTAL_SCORE: "231,265",
    }
    return ntc_stats.StatColumns(**stats_dict)  # type: ignore


@pytest.fixture
def woodster_stats() -> ntc_stats.StatColumns:
    stats_dict = {
        ntc_stats.KD_RATIO: "0.83",
        ntc_stats.WIN_PERC: "69.6%",
        ntc_stats.SCORE_PER_MIN: "336.91",
        ntc_stats.KILLS: "429",
        ntc_stats.DEATHS: "519",
        ntc_stats.WINS: "16",
        ntc_stats.LOSSES: "7",
        ntc_stats.TIES: "0",
        ntc_stats.ASSISTS: "41",
        ntc_stats.BEST_KILLSTREAK: "15",
        ntc_stats.AVG_LIFESPAN: "27.982s",
        ntc_stats.TOTAL_SCORE: "81,550",
    }
    return ntc_stats.StatColumns(**stats_dict)  # type: ignore


@pytest.fixture
def stat_list(
    joy_stats: ntc_stats.StatColumns,
    askinner_stats: ntc_stats.StatColumns,
    unwitty_stats: ntc_stats.StatColumns,
    clicky_stats: ntc_stats.StatColumns,
    cali_stats: ntc_stats.StatColumns,
    woodster_stats: ntc_stats.StatColumns,
) -> list[ntc_stats.StatColumns | dict | None]:
    return [
        joy_stats,
        askinner_stats,
        unwitty_stats,
        clicky_stats,
        {},
        cali_stats,
        woodster_stats,
        {},
        None,
    ]
