import os

basedir = os.path.abspath(os.path.dirname(__file__))
# instance_path = os.path.join(os.path.dirname(basedir), 'instance') # Not typically needed for MySQL
# os.makedirs(instance_path, exist_ok=True) # Not needed unless storing other files there

# Function to build the MySQL URI safely
def get_mysql_uri():
    # Prioritize DATABASE_URL if set (common for hosting platforms)
    env_uri = os.environ.get('DATABASE_URL')
    if env_uri:
         # Heroku/some platforms might use postgresql://, ensure it's mysql://
        if env_uri.startswith("postgres://"):
            # Basic conversion attempt, may need adjustment
            env_uri = env_uri.replace("postgres://", "mysql+mysqlclient://", 1)
        return env_uri

    # Otherwise, build from individual environment variables
    host = os.environ.get('DB_HOST', 'localhost') # Default to localhost
    port = os.environ.get('DB_PORT', '3306')      # Default MySQL port
    database = os.environ.get('DB_NAME', 'your_database_name') # Use the name you created
    user = os.environ.get('DB_USER', 'your_app_user')     # Use the user you created
    password = os.environ.get('DB_PASSWORD', None)        # Get password from environment

    if not password:
        raise ValueError("DB_PASSWORD environment variable not set.")

    # Choose driver based on what you installed
    driver = "mysql+pymysql"  # Using PyMySQL instead of mysqlclient

    return f"{driver}://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4"

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'

    # Use SQLite database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional: Add engine options if needed, e.g., pool recycling
    # SQLALCHEMY_ENGINE_OPTIONS = {
    #    "pool_recycle": 280, # Recycle connections older than 280 seconds
    #    "pool_pre_ping": True # Check connection validity before use
    # }