import requests
import json

def get_api_token(vanity_domain, client_id, client_secret):
    token_url = f"https://{vanity_domain}.zslogin.net/oauth2/v1/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": "https://api.zscaler.com"
    }

    try:
        response = requests.post(token_url, data=payload, headers=headers)
        print(f"\n[DEBUG] Status Code: {response.status_code}")
        print(f"[DEBUG] Raw Response: {response.text}")
        response.raise_for_status()

        token_data = response.json()
        access_token = token_data.get("access_token")
        expires_in = token_data.get("expires_in")

        if access_token:
            print("Access token obtained successfully.")
            print(f"Token expires in {expires_in} seconds.\n")
            return access_token
        else:
            print("Failed to retrieve access token.")
            return None

    except requests.exceptions.RequestException as e:
        print("Error during token request:", e)
        if response is not None:
            print(f"Response content: {response.text}")
        return None

def call_api_with_token(token):
    while True:
        endpoint_url = input("\nEnter full API endpoint URL (or type 'exit' to quit): ").strip()
        if endpoint_url.lower() == "exit":
            print("Exiting API client.")
            break
            
        method = input("Enter HTTP method (GET/POST) [default POST]: ").strip().upper() or "POST"

        raw_payload = input("Enter JSON payload (leave blank for none): ").strip()

        # Validate JSON payload if provided
        if raw_payload:
            try:
                json_payload = json.loads(raw_payload)
                payload = json.dumps(json_payload)  # Properly serialized string
            except json.JSONDecodeError as e:
                print("Invalid JSON. Please check formatting.")
                continue
        else:
            payload = None

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        try:
            if method == "GET":
                response = requests.get(endpoint_url, headers=headers, params=json_payload if payload else {})
            else:  # POST (or default)
                response = requests.post(endpoint_url, headers=headers, data=payload)

            print(f"\n[DEBUG] Status Code: {response.status_code}")
            print(f"[DEBUG] Raw Response: {response.text}")

            response.raise_for_status()

            try:
                print("API Response (formatted):")
                print(json.dumps(response.json(), indent=2))
            except ValueError:
                print("Non-JSON response:")
                print(response.text)

        except requests.exceptions.RequestException as e:
            print("Error while calling API:", e)
        

def main():
    print("=== Simple OneAPI Client ===")
    use_existing_token = input("Do you already have a valid token? (yes/no): ").strip().lower()

    if use_existing_token == "yes":
        token = input("Enter your Bearer token: ").strip()
    else:
        vanity_domain = input("Enter your Zscaler Vanity Domain: ").strip()
        client_id = input("Enter Client ID: ").strip()
        client_secret = input("Enter Client Secret: ").strip()
        token = get_zscaler_token(vanity_domain, client_id, client_secret)

    if token:
        call_api_with_token(token)
    else:
        print("Could not proceed without a valid token.")

if __name__ == "__main__":
    main()
