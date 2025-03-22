from app.config.db import Base, engine

print("Creating database table...")
Base.metadata.create_all(bind=engine)
print("Database table created!")