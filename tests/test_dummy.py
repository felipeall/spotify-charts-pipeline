from sqlalchemy import select

from src.models.user import User


def test_dummy():
    assert True


def test_user_created(db_session):
    db_session.add(User(name="Jane Doe"))
    db_session.commit()

    result = db_session.execute(select(User).filter_by(name="Jane Doe"))
    res = result.scalars().first()

    assert res == 1
