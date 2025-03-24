import random

from ..models.users import DbUser

fake_users_db = {
    "user@example.com": {
        "id": 1,
        "email": "user@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }
}


def get_user(email: str) -> DbUser:
    user_dict = fake_users_db.get(email)
    if user_dict:
        return DbUser(**user_dict)


def create_user(
        email: str,
        hashed_password: str,
) -> DbUser:
    user_id = random.randint(1, 1000)

    db_user = DbUser(id=user_id, email=email, hashed_password=hashed_password)
    fake_users_db[email] = db_user.__dict__

    return db_user
