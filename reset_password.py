# reset_password.py
import json, hashlib

email = "info@halalbot.app"
new_password = "#062308Ghada!"
hashed = hashlib.sha256(new_password.encode()).hexdigest()

with open("users.json", "r") as f:
    users = json.load(f)

if email in users:
    users[email]["password"] = hashed
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)
    print("✅ Password reset for", email)
else:
    print("❌ Email not found.")
