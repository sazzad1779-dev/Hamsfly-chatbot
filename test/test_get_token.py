from src.api_call.auth_token_create import SabreAuthClient
from dotenv import load_dotenv
import os
load_dotenv(override=True)
sabre_client = SabreAuthClient(os.getenv("encoded_secret",""), is_production=True)
new_token = sabre_client.get_token()
## already in .env file access_token mentioned i want to update it with new token
with open(".env", "r") as f:
    lines = f.readlines()
with open(".env", "w") as f:
    for line in lines:
        if line.startswith("access_token="):
            f.write(f"access_token={new_token}\n")
        else:
            f.write(line)
print("✅ Access token updated in .env")