from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()
print ("inside of init.py")

def create_app():
    print("in create app")
    app = Flask(__name__,instance_relative_config=True)
    db_name = 'Trendscope.db'
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "Testdb.sqlite"),
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    
    from . import db
    db.init_app(app)
    #migrate.init_app(app, db)
    return app