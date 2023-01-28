from src.models.tracks import Tracks


def test_track_created(db_session, get_random_string, get_today_date, count_records_table):
    track = Tracks(
        trackUri=get_random_string,
        trackName=get_random_string,
        displayImageUri=get_random_string,
        artistUri=[get_random_string],
        labels=[get_random_string],
        releaseDate=get_today_date,
    )
    db_session.add(track)
    db_session.commit()

    assert count_records_table(Tracks)
