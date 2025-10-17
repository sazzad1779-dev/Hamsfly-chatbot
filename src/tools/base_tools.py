from src.api_call.flight_search import SabreFlightSearch
sabre_flight_search = SabreFlightSearch()
from agno.tools import tool
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
    return sabre_flight_search.search(pcc, origin, destination, start_date, end_date)
