from flask import Flask
from config import passcode
from datetime import timedelta
import os.path
app = Flask(__name__)
app.config['SECRET_KEY'] = passcode
app.config['TEMP_IMG_PATH'] = "/static/image"
app.permanent_session_lifetime = timedelta(minutes=5)
import auth
import index
import account

app.register_blueprint(auth.bp)
app.register_blueprint(index.bp)	
app.register_blueprint(account.bp)


if __name__ == '__main__':
	app.run(debug=True)