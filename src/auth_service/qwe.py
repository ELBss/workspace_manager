from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the base class for declarative class definitions
Base = declarative_base()

# Define the UserAuth class with the table structure


class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    nickname = Column(String)
    role = Column(String)


# Create an engine to connect to the SQLite database
# Replace with your database file path
engine = create_engine('sqlite:///user_auth.db')

# Create a sessionmaker bound to the engine
Session = sessionmaker(bind=engine)
session = Session()

# Query the database to retrieve the data
user_auth_data = session.query(UserRole).all()

# Print the retrieved data
for user in user_auth_data:
    print(f"ID: {user.user_id}, nick: {user.nickname}, role: {user.role}")

# Reflect the existing database
metadata = MetaData()
metadata.reflect(bind=engine)

# Close the session
session.close()
