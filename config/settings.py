# Flask
DEBUG = True
SERVER_NAME = "localhost:8000"

# SQLAlchemy
db_uri = 'postgresql://mta_tracker:devpassword@postgres:5432/mta_tracker'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False