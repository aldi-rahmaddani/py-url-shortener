from app.models.base import Base, engine

print("Creating database table...")
Base.metadata.create_all(bind=engine)
print("Database table created!")