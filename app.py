import os
import smtplib
from email.message import EmailMessage

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# --------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------
load_dotenv()


EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# --------------------
# FLASK APP
# --------------------
app = Flask(__name__)

# --------------------
# EMAIL FUNCTION
# --------------------
def send_email(name, email, message):
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

        # IMPORTANT: timeout added
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully")

    except Exception as e:
        # Log error but DO NOT crash the app
        print("Email failed:", str(e))

# --------------------
# ROUTES
# --------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not name or not email or not message:
        return jsonify({"success": False, "error": "Missing fields"}), 400

    # Save message to file
    with open("messages.txt", "a", encoding="utf-8") as file:
        file.write("----- NEW MESSAGE -----\n")
        file.write(f"Name: {name}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Message: {message}\n")
        file.write("\n")

    # Send email notification
    send_email(name, email, message)
    return jsonify({"success": True})



# --------------------
# RUN APP
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
