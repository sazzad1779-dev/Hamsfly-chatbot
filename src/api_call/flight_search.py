import requests
import json

class SabreFlightSearch:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.url = "https://api.platform.sabre.com/v4.3.0/shop/flights?mode=live"

    def search(self, pcc: str,origin: str, destination: str, start_date: str, end_date: str):
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        body = {
            "OTA_AirLowFareSearchRQ": {
                "Version": "4.3.0",
                "POS": {
                    "Source": [
                        {
                            "PseudoCityCode": pcc,
                            "RequestorID": {
                                "Type": "1",
                                "ID": "1",
                                "CompanyName": {
                                    "Code": "TN",
                                    "content": "TN"
                                }
                            }
                        }
                    ]
                },
                "OriginDestinationInformation": [
                    {
                        "RPH": "1",
                        "DepartureDateTime": f"{start_date}T11:00:00",
                        "OriginLocation": {"LocationCode": origin},
                        "DestinationLocation": {"LocationCode":destination}
                    },
                    {
                        "RPH": "2",
                        "DepartureDateTime": f"{end_date}T11:00:00",
                        "OriginLocation": {"LocationCode":destination},
                        "DestinationLocation": {"LocationCode": origin}
                    }
                ],
                "TravelPreferences": {
                    "ValidInterlineTicket": True,
                    "FlightTypePref": {"MaxConnections": "0"}
                },
                "TravelerInfoSummary": {
                    "SeatsRequested": [1],
                    "AirTravelerAvail": [
                        {
                            "PassengerTypeQuantity": [
                                {"Code": "ADT", "Quantity": 1}
                            ]
                        }
                    ]
                },
                "TPA_Extensions": {
                    "IntelliSellTransaction": {
                        "RequestType": {"Name": "50ITINS"}
                    }
                }
            }
        }

        response = requests.post(self.url, headers=headers, json=body)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            return None


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    import os
    load_dotenv()
    access_token = os.getenv("ACCESS_TOKEN")
    sabre = SabreFlightSearch(access_token)
    result = sabre.search(
        pcc="7C18",  
        origin="MIA",
        destination= "MCO"    ,        # Replace with your PseudoCityCode
        start_date="2025-10-10",
        end_date="2025-10-20"
    )

    if result:
        from pprint import pprint
        pprint(result)
