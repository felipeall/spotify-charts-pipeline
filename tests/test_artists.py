from src.models.artists import Artists


def test_artist_created(db_session, get_random_string, count_records_table):
    artist = Artists(
        uri=get_random_string,
        name=get_random_string,
    )
    db_session.add(artist)
    db_session.commit()

    assert count_records_table(Artists)
