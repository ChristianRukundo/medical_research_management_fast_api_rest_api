# from faker import Faker
# from faker.generator import random
# from sqlalchemy.orm import Session
# import sys
#
# from ..models.research import Research
# from ..models.users import User
#
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os
#
# SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local.db")
#
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
#
# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
#
# Base = declarative_base()
#
#
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# # Initialize Faker and create database session
# fake = Faker()
#
#
# # Function to create a user
# def create_user_batch(batch_size: int):
#     users = []
#     for _ in range(batch_size):
#         name = fake.name()
#         email = fake.email()
#         password = fake.password()
#
#         user = User(name=name, email=email, password=password)
#         users.append(user)
#     return users
#
#
# # Function to create research
# def create_research_batch(db: Session, user_ids: list, batch_size: int):
#     researches = []
#     for _ in range(batch_size):
#         title = fake.sentence(nb_words=6)
#         description = fake.text(max_nb_chars=200)
#         cost = random.uniform(1000, 50000)  # Random cost between 1000 and 50000
#         duration_in_days = random.randint(30, 365)  # Random duration between 30 and 365 days
#         category = random.choice(["Health", "AI", "Business", "Technology", "Environment"])
#         is_published = random.choice([True, False])
#         date_created = fake.date_this_decade()
#
#         user_id = random.choice(user_ids)  # Randomly select a user
#
#         research = Research(
#             title=title,
#             description=description,
#             cost=cost,
#             duration_in_days=duration_in_days,
#             category=category,
#             is_published=is_published,
#             date_created=date_created,
#             creator_id=user_id
#         )
#         researches.append(research)
#
#     return researches
#
#
# # Function to populate the database with users and research projects using batching
# def populate_db(batch_size=1000, total_users=500000, total_researches=500000):
#     db = SessionLocal()
#     try:
#         # Create users in batches
#         print("Populating users...")
#         for _ in range(total_users // batch_size):
#             users = create_user_batch(batch_size)
#             db.add_all(users)
#             db.commit()  # Commit after each batch
#             print(f"{len(users)} users added")
#
#         # Create research projects in batches
#         print("Populating research projects...")
#         users = db.query(User).all()  # Fetch all users to randomly assign them
#         user_ids = [user.id for user in users]
#
#         for _ in range(total_researches // batch_size):
#             researches = create_research_batch(db, user_ids, batch_size)
#             db.add_all(researches)
#             db.commit()  # Commit after each batch
#             print(f"{len(researches)} research projects added")
#
#         print("Database populated successfully!")
#
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         db.close()
#
#
# # Execute the population script
# if __name__ == "__main__":
#     populate_db()  # Adjust batch_size if necessary
