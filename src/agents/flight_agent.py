import os
import requests
import json
from agno.agent import Agent
from agno.tools import tool
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()

@tool()
def search_sabre_flights(
    pcc: str,
    origin: str, 
    destination: str, 
    start_date: str, 
    end_date: str
) -> str:
    """Search for round-trip flights using Sabre API
    
    Args:
        pcc: Pseudo City Code for Sabre
        origin: Origin airport code (e.g., 'MIA')
        destination: Destination airport code (e.g., 'MCO')
        start_date: Departure date (YYYY-MM-DD)
        end_date: Return date (YYYY-MM-DD)
    """
    access_token = os.getenv("ACCESS_TOKEN")
    url = "https://api.platform.sabre.com/v4.3.0/shop/flights?mode=live"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    body = {
        "OTA_AirLowFareSearchRQ": {
            "Version": "4.3.0",
            "POS": {
                "Source": [{
                    "PseudoCityCode": pcc,
                    "RequestorID": {
                        "Type": "1",
                        "ID": "1",
                        "CompanyName": {"Code": "TN", "content": "TN"}
                    }
                }]
            },
            "OriginDestinationInformation": [
                {
                    "RPH": "1",
                    "DepartureDateTime": f"{start_date}T11:00:00",
                    "OriginLocation": {"LocationCode": origin},
                    "DestinationLocation": {"LocationCode": destination}
                },
                {
                    "RPH": "2", 
                    "DepartureDateTime": f"{end_date}T11:00:00",
                    "OriginLocation": {"LocationCode": destination},
                    "DestinationLocation": {"LocationCode": origin}
                }
            ],
            "TravelPreferences": {
                "ValidInterlineTicket": True,
                "FlightTypePref": {"MaxConnections": "0"}
            },
            "TravelerInfoSummary": {
                "SeatsRequested": [1],
                "AirTravelerAvail": [{
                    "PassengerTypeQuantity": [{"Code": "ADT", "Quantity": 1}]
                }]
            },
            "TPA_Extensions": {
                "IntelliSellTransaction": {"RequestType": {"Name": "50ITINS"}}
            }
        }
    }

    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        return json.dumps(response.json(), indent=2)
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# Create your Sabre flight agent
sabre_agent = Agent(
    name="Sabre Flight Search Agent",
    model=OpenAIChat(id="gpt-4"),
    tools=[search_sabre_flights],
    instructions=[
        "You are a flight search specialist using Sabre APIs",
        "Help users find flights with clear pricing and schedules",
        "Always ask for required parameters: PCC, origin, destination, dates"
    ],
    markdown=True
)

# Test the agent
sabre_agent.print_response(
    "Search for flights from MIA to MCO departing 2025-10-10 and returning 2025-10-20, use PCC 7C18"
)