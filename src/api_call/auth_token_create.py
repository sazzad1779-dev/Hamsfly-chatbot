import requests

class SabreAuthClient:
    def __init__(self, encoded_secret: str, is_production: bool = True):
        """
        Initialize the SabreAuthClient.

        :param encoded_secret: Base64 encoded string of 'username:password:domain:organization'
        :param is_production: Use production endpoint if True, sandbox otherwise
        """
        self.encoded_secret = encoded_secret
        self.url = (
            "https://api.sabre.com/v2/auth/token"
            if is_production else
            "https://api-crt.cert.havail.sabre.com/v2/auth/token"
        )

    def get_token(self):
        """
        Request an OAuth access token from Sabre.

        :return: Access token string or None if failed
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self.encoded_secret}"
        }

        data = "grant_type=client_credentials"

        try:
            response = requests.post(self.url, headers=headers, data=data)
            if response.status_code == 200:
                token = response.json().get("access_token")
                print("✅ Access Token:", token)
                return token
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return None
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return None

    def search_flights(self, origin: str, destination: str,
                    departure_date: str, return_date: str = None,
                    passengers: int = 1, cabin: str = "Y"):
            """
            Perform a flight search.

            :param origin: IATA code (e.g., 'JFK')
            :param destination: IATA code (e.g., 'LHR')
            :param departure_date: 'YYYY-MM-DD'
            :param return_date: 'YYYY-MM-DD' (optional for round trips)
            :param passengers: number of passengers
            :param cabin: cabin type (Y = Economy, C = Business, F = First)
            """
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }

            payload = {
                "OTA_AirLowFareSearchRQ": {
                    "OriginDestinationInformation": [
                        {
                            "DepartureDateTime": departure_date,
                            "OriginLocation": {"LocationCode": origin},
                            "DestinationLocation": {"LocationCode": destination}
                        }
                    ],
                    "TravelPreferences": {
                        "CabinPref": [{"Cabin": cabin}]
                    },
                    "TravelerInfoSummary": {
                        "AirTravelerAvail": [
                            {
                                "PassengerTypeQuantity": [
                                    {"Code": "ADT", "Quantity": passengers}
                                ]
                            }
                        ]
                    }
                }
            }

            # Add return leg if needed
            if return_date:
                payload["OTA_AirLowFareSearchRQ"]["OriginDestinationInformation"].append({
                    "DepartureDateTime": return_date,
                    "OriginLocation": {"LocationCode": destination},
                    "DestinationLocation": {"LocationCode": origin}
                })

            response = requests.post(self.url, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return None