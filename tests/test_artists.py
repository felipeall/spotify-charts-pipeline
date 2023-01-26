from sqlalchemy import func, select

from src.models.artists import Artists
from tests.utils import generate_random_string


def test_artist_created(db_session):
    uri = generate_random_string()
    name = generate_random_string()

    artist = Artists(
        uri=uri,
        name=name,
    )
    db_session.add(artist)
    db_session.commit()

    result = db_session.execute(select(func.count()).select_from(Artists).filter_by(uri=uri, name=name))

    assert result.scalars().one()
