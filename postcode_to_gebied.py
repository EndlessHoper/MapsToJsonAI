import requests

def get_gebied_from_postcode(postcode):
    """
    Given a postcode, this function retrieves the corresponding "gebied" in Amsterdam.
    Args:
        postcode (str): The Dutch postcode (e.g., "1103JT").

    Returns:
        str: The name of the "gebied" or an error message.
    """
    try:
        # Step 1: Query the PDOK Locatieserver API
        locatieserver_url = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/suggest"
        locatieserver_params = {
            "fl": "id,weergavenaam,straatnaam,huis_nlt,postcode,woonplaatsnaam,centroide_ll,adresseerbaarobject_id,nummeraanduiding_id",
            "fq": ["bron:BAG", "type:adres", "woonplaatsnaam:(amsterdam,weesp)", "gemeentenaam:amsterdam"],
            "q": postcode
        }
        locatieserver_response = requests.get(locatieserver_url, params=locatieserver_params)

        if locatieserver_response.status_code != 200:
            return f"Error querying Locatieserver: {locatieserver_response.status_code}"

        locatieserver_data = locatieserver_response.json()
        if not locatieserver_data["response"]["docs"]:
            return "No address found for the given postcode."

        nummeraanduiding_id = locatieserver_data["response"]["docs"][0].get("nummeraanduiding_id")

        if not nummeraanduiding_id:
            return "nummeraanduiding_id not found in Locatieserver response."

        # Step 2: Query the Amsterdam Data API for nummeraanduiding details
        amsterdam_data_url = f"https://api.data.amsterdam.nl/bag/v1.1/nummeraanduiding/?landelijk_id={nummeraanduiding_id}&detailed=1"
        amsterdam_data_response = requests.get(amsterdam_data_url)

        if amsterdam_data_response.status_code != 200:
            return f"Error querying Amsterdam Data API: {amsterdam_data_response.status_code}"

        amsterdam_data = amsterdam_data_response.json()
        if not amsterdam_data.get("results"):
            return "No data found in Amsterdam Data API response."

        gebied_info = amsterdam_data["results"][0].get("gebiedsgerichtwerken")
        if not gebied_info:
            return "No gebied information found in Amsterdam Data API response."

        gebied_name = gebied_info.get("_display")
        return gebied_name if gebied_name else "Gebied name not found in API response."

    except Exception as e:
        return f"An error occurred: {e}"

# Main execution
def main():
    try:
        postcode = input("Please enter the postcode: ").strip()
        if not postcode:
            raise ValueError("Postcode cannot be empty. Please provide a valid postcode.")

        gebied = get_gebied_from_postcode(postcode)
        print(f"The gebied for postcode {postcode} is: {gebied}")
    except ValueError as ve:
        print(f"Input Error: {ve}")
    except OSError as oe:
        print(f"System Error: {oe}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
