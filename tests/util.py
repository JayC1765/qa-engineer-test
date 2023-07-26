from models.users import User


# Helper function to add a n # of unique users to the database
def add_users_to_db(db, num):
    for i in range(num):
        username = f"user{i}"
        new_user = User(username=username)
        db.add(new_user)

    db.commit()
    db.refresh(new_user)
