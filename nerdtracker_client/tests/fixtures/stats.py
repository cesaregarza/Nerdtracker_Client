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
