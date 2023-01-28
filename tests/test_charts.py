from src.models.charts import Charts


def test_chart_created(db_session, get_random_string, get_today_date, count_records_table):
    chart = Charts(
        uri=get_random_string,
        alias=get_random_string,
        entityType=get_random_string,
        readableTitle=get_random_string,
        backgroundColor=get_random_string,
        textColor=get_random_string,
        latestDate=get_today_date,
        earliestDate=get_today_date,
        country=get_random_string,
        chartType=get_random_string,
        recurrence=get_random_string,
    )
    db_session.add(chart)
    db_session.commit()

    assert count_records_table(Charts)
