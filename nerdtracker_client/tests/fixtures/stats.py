import pytest

import nerdtracker_client.constants.stats as ntc_stats


@pytest.fixture
def stats() -> ntc_stats.StatColumns:
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
