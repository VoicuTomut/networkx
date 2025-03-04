import requests
import re

def extract_location_coordinates(address_string):
    """
        Extract coordinates from a string in the format:
        "123 Main Street, New York, NY [40.7128, -74.0060]"

        Args:
            address_string (str): The address string containing coordinates

        Returns:
            list: A list of two floats [lat, lng] if coordinates are found, None otherwise
        """
    # Regular expression to match coordinates in square brackets
    pattern = r'\[([-]?\d+\.?\d*),\s*([-]?\d+\.?\d*)\]'

    # Search for the pattern in the address string
    match = re.search(pattern, address_string)

    # If coordinates are found, return them as floats
    if match:
        return [float(match.group(1)), float(match.group(2))]

    # Return None if no coordinates are found
    return None


def check_coordinates(phone, location):

    url = "https://location-verification.p-eu.rapidapi.com/verify"
    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "location-verification.nokia.rapidapi.com",
        "x-rapidapi-key": "3aa9d376cfmsh16446717213dd03p1e3dfdjsn0c3cc2207d6f"
    }

    data = {
        "device": {
            "phoneNumber": phone
        },
        "area": {
            "areaType": "CIRCLE",
            "center": {
                "latitude": location[0],
                "longitude": location[1]
            },
            "radius": 2000
        },
        "maxAge": 100}

    response = requests.post(url, headers=headers, json=data)

    print("Coordinates response:", response.json())
    response=response.json().get("verificationResult")
    if response=="FALSE":
        response=False
    elif response=="TRUE":
        response = True
    return response





