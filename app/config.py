import os

class Config(object):

    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Google Cloud SQL (change this accordingly)
    PASSWORD = os.environ.get('SECRET_KEY')
    PUBLIC_IP_ADDRESS = os.environ.get('SECRET_KEY')
    DBNAME = os.environ.get('SECRET_KEY')
    PROJECT_ID = os.environ.get('SECRET_KEY')
    INSTANCE_NAME = os.environ.get('SECRET_KEY')

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket =/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}"
    

    