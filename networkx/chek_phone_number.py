import requests
import urllib.parse

APIK="3aa9d376cfmsh16446717213dd03p1e3dfdjsn0c3cc2207d6f"

def get_client_credentials():
    url = "https://nac-authorization-server.p-eu.rapidapi.com/auth/clientcredentials"
    headers = {
        "X-RapidAPI-Host": "nac-authorization-server.nokia.rapidapi.com",
        "X-RapidAPI-Key": APIK
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching client credentials:", response.text)
        return None



def generate_authorization():
    url = "https://well-known-metadata.p-eu.rapidapi.com/openid-configuration"
    headers = {
        "X-RapidAPI-Host": "well-known-metadata.nokia.rapidapi.com",
        "X-RapidAPI-Key": APIK
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching authorization:", response.text)
        return None


def get_confirm_link(
        authorization_endpoint,
        client_id,
        login_hint,
        redirect_uri,
        response_type="code",
        scope="dpv:FraudPreventionAndDetection%23number-verifcation-verify-read",
        state="c3VwZXItc2VjcmV0"
):
    """
    Generate a confirmation link for number verification OAuth flow.

    This function creates the direct URL that will redirect to Nokia's authorization server
    for number verification.

    Args:
        authorization_endpoint (str): Authorization server URL (e.g., "https://auth-us-east-1.nacruntime-sm.nwac-dev.net/oauth2/v1/authorize")
        client_id (str): Client ID for the application
        login_hint (str): The end-user phone number (e.g., "tel:+40757796991")
        redirect_uri (str): Application backend endpoint for receiving the authorization callback
        response_type (str, optional): Response type, must be "code". Defaults to "code".
        scope (str, optional): Consent scope. Defaults to "number-verification:verify".
        state (str, optional): Value to maintain state between request and callback. Defaults to "c3VwZXItc2VjcmV0".

    Returns:
        str: The full authorization URL that should be presented to the user
    """
    # Create the direct URL that will initiate the Nokia authorization flow

    encoded_login_hint = urllib.parse.quote(login_hint)
    state = encoded_login_hint

    # Create the direct URL that will initiate the Nokia authorization flow
    auth_link = f"{authorization_endpoint}?scope={scope}&state={state}&response_type={response_type}&client_id={client_id}&redirect_uri={redirect_uri}&login_hint={encoded_login_hint}"

    return auth_link


def get_access_token(client_id, client_secret, auth_code):
    url = "https://auth-us-east-1.nacruntime-sm.nwac-dev.net/oauth2/v1/token"
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": auth_code
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print("Error fetching access token:", response.text)
        return None


def verify_phone_number(access_token, phone_number):
    url = "https://number-verification.api.endpoint/verify"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {"phoneNumber": phone_number}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        verification_result = response.json()
        if verification_result.get("devicePhoneNumberVerified"):
            return "Correct phone number."
        else:
            return "Not the same."
    elif response.status_code == 404:
        return "Unknown device ID."
    else:
        return f"Error verifying phone number: {response.text}"


def main():
    credentials = get_client_credentials()
    authorization = generate_authorization()
    print("we have credentials:{}".format(credentials))
    print("we have authorization: {}".format(authorization))

    if credentials and authorization:
        client_id = credentials.get("client_id")
        client_secret = credentials.get("client_secret")

        authorization_endpoint = authorization.get("authorization_endpoint")
        token_endpoint = authorization.get("token_endpoint")


        redirect_uri = "https://example.com/redirect"
        login_hint = "+40757796991"  # Example phone number

        auth_link = get_confirm_link(
                                        authorization_endpoint,
                                        client_id,
                                        login_hint,
                                        redirect_uri,
                                        response_type="code",

                                )



        print("authorization link: {}".format(auth_link))

        auth_code = input("Enter the received authorization code from the redirect URL: ", )

        if auth_code:
            access_token = get_access_token(client_id, client_secret, auth_code)
            if access_token:
                verification_message = verify_phone_number(access_token, login_hint)
                print(verification_message)
            else:
                print("Failed to retrieve access token.")
        else:
            print("No authorization code received.")
    else:
        print("Failed to retrieve client credentials.")


if __name__ == "__main__":
    main()
