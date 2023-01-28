from src.models.ranks import Ranks


def test_rank_created(db_session, get_random_string, get_today_date, get_random_int, count_records_table):
    rank = Ranks(
        chartUri=get_random_string,
        date=get_today_date,
        trackUri=get_random_string,
        currentRank=get_random_int,
        previousRank=get_random_int,
        peakRank=get_random_int,
        appearancesOnChart=get_random_int,
        consecutiveAppearancesOnChart=get_random_int,
        metricValue=get_random_int,
        metricType=get_random_string,
        entryStatus=get_random_string,
        peakDate=get_today_date,
        entryRank=get_random_int,
        entryDate=get_today_date,
    )
    db_session.add(rank)
    db_session.commit()

    assert count_records_table(Ranks)
