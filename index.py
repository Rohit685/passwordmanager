from flask import Blueprint, render_template,request,flash,session, url_for, g, redirect
import webbrowser
bp = Blueprint("index", __name__)


@bp.route("/")
def index():
	return render_template("index.html")

@bp.route("/rickroll")
def rickroll():
	#webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
	return render_template("rickroll.html")