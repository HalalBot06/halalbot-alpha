# one_time_upgrade_users_json.py
import json

with open("users.json", "r") as f:
    old_users = json.load(f)

new_users = {}
for email, hashed_pw in old_users.items():
    new_users[email] = {
        "password": hashed_pw,
        "invite_code": "legacy",
        "is_admin": False
    }

with open("users.json", "w") as f:
    json.dump(new_users, f, indent=2)

print("✅ Converted users.json to new format.")
