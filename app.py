import os
import smtplib
import threading
from email.message import EmailMessage
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load env vars
load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)

# --------------------
# BACKGROUND EMAIL SENDER
# --------------------
def send_email_background(name, email, message):
    try:
        msg = EmailMessage()
        msg["Subject"] = "New Contact Message"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS
        msg.set_content(
            f"""
New message from your portfolio website:

Name: {name}
Email: {email}

Message:
{message}
"""
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully")

    except Exception as e:
        print("Email failed:", e)

# --------------------
# ROUTES
# --------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"success": False}), 400

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"success": False}), 400

    # Start email in background (NON-BLOCKING)
    thread = threading.Thread(
        target=send_email_background,
        args=(name, email, message),
        daemon=True
    )
    thread.start()

    # IMMEDIATE RESPONSE — no waiting
    return jsonify({"success": True})

# --------------------
# RUN
# --------------------
if __name__ == "__main__":
    app.run()
