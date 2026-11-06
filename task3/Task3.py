
import os
import requests
import hmac
import hashlib

from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Load environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

# Create API session with retry
session = requests.Session()

retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry)
session.mount("https://", adapter)

# API request
url = "https://jsonplaceholder.typicode.com/users"

response = session.get(
    url,
    headers={"X-API-Key": API_KEY},
    timeout=15
)

response.raise_for_status()
users = response.json()

# Print first 5 users
print("First 5 Users:")

for user in users[:5]:
    print(
        user.get("id"),
        "-",
        user.get("name"),
        "-",
        user.get("email")
    )

# First user's nested details
first_user = users[0]

address = first_user.get("address", {})
geo = address.get("geo", {})
company = first_user.get("company", {})

print("\nFirst User Details:")
print("City:", address.get("city", "Not Available"))
print("Latitude:", geo.get("lat", "Not Available"))
print("Zip:", address.get("zipcode", "Not Available"))
print("Company:", company.get("name", "Not Available"))

# HMAC signature verification
def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)


# Test webhook security
payload = b"employee data"

valid_signature = hmac.new(
    WEBHOOK_SECRET.encode(),
    payload,
    hashlib.sha256
).hexdigest()

tampered_payload = b"changed employee data"

wrong_signature = hmac.new(
    b"wrong_secret",
    payload,
    hashlib.sha256
).hexdigest()

print("\nWebhook Validation:")
print(
    "Valid:",
    verify_signature(payload, valid_signature, WEBHOOK_SECRET),
    "| Tampered:",
    verify_signature(tampered_payload, valid_signature, WEBHOOK_SECRET),
    "| Wrong secret:",
    verify_signature(payload, wrong_signature, WEBHOOK_SECRET)
)
