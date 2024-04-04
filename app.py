import os
from validators import email as validate_email
from flask_httpauth import HTTPBasicAuth
import html
import send
from flask import Flask, render_template, request, jsonify

sec = os.environ.get("KEY")

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
	if username == 'admin' and password == sec:
		return True
	else:
		return False

import subs

app = Flask(__name__)

@app.route('/api/remSub', methods=['POST'])
@auth.login_required
def rem_subscriber():
	email = request.get_json().get("email")
	if email and validate_email(email):
		try:
			if subs.removeSubscriber(email):
				return jsonify(success=True)
			else:
				return jsonify(success=True, message="Email not subscribed")
		except:
			return jsonify(success=False, message="Error")
	else:
		return jsonify(success="error", message="No email provided")


@app.route('/')
@auth.login_required
def index():
	return render_template("index.jinja")

@app.route("/api/newSub", methods=["POST"])
@auth.login_required
def newSub():
	email = request.get_json().get("email")
	if email and validate_email(email):
		try:
			if subs.addSubscriber(email):
				return jsonify(success=True)
			else:
				return jsonify(success=True, message="Email already subscribed")
		except Exception as e:
			print(e)
			return jsonify(success=False, message="Error")
	else:
		return jsonify(success="error", message="No email provided")
@app.route("/all_subs")
@auth.login_required
def all_subs():
	if request.method == "GET":
		subsC = subs.getAllSubs()
		le = len(subsC)
		return render_template("all_subs.jinja", subs=subsC, subsLength=le)
	if request.method == "POST":
	 	return jsonify(subs.getAllSubs())


@app.route("/new_email",methods=["POST", "GET"])
@auth.login_required
def new_email():
	if request.method == "GET":
		return render_template("new_email.jinja")
	if request.method == "POST":
		try:
			subject = request.get_json().get("subject")
			message = request.get_json().get("message")
			message = html.unescape(message)
			allEmails = subs.getEmails()
			send.send(allEmails, subject, message)
			print("Mails should be sent to everyone soon.")
		except Exception as e:
			print(e)
			return jsonify(False)
		return jsonify(True)


if __name__ == '__main__':
	app.run(debug=True)
