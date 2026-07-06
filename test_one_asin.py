import os
from dotenv import load_dotenv
from sp_api.api import ListingsRestrictions
from sp_api.base import Marketplaces, SellingApiException

load_dotenv()

SELLER_ID = os.getenv("SELLER_ID")
MARKETPLACE_ID = os.getenv("MARKETPLACE_ID", "A2EUQ1WTGCTBG2")

credentials = {
    "refresh_token": os.getenv("REFRESH_TOKEN"),
    "lwa_app_id": os.getenv("LWA_APP_ID"),
    "lwa_client_secret": os.getenv("LWA_CLIENT_SECRET"),
    "aws_access_key": os.getenv("AWS_ACCESS_KEY_ID"),
    "aws_secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
}

def check_restrictions(asin: str):
    api = ListingsRestrictions(
        marketplace=Marketplaces.CA,
        credentials=credentials
    )

    response = api.get_listings_restrictions(
        asin=asin,
        sellerId=SELLER_ID,
        marketplaceIds=[MARKETPLACE_ID],
        conditionType="new_new"
    )

    payload = response.payload
    restrictions = payload.get("restrictions", [])

    print("\nASIN:", asin)
    print("Raw response:")
    print(payload)

    if restrictions:
        print("\nResult: YES - restricted/gated or approval may be required.")
    else:
        print("\nResult: NO - no listing restriction returned.")

if __name__ == "__main__":
    asin = input("Enter an Amazon.ca ASIN to test: ").strip().upper()

    try:
        check_restrictions(asin)
    except SellingApiException as error:
        print("\nAmazon SP-API error:")
        print(error)
    except Exception as error:
        print("\nUnexpected error:")
        print(error)