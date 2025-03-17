import requests
from celery import shared_task
from . import models


@shared_task(bind=True)
def fetch_crypto_prices(self):
    third_party_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    response = requests.get(third_party_url)

    if response.status_code == 200:
        data = response.json()
        btc_price = data["bitcoin"]["usd"]
        eth_price = data["ethereum"]["usd"]

        # Example org_ids (You should fetch these dynamically)

        org_ids = models.Organisation.objects.all()
        print(org_ids)


        for org_id in org_ids:
            models.CryptoPriceModel.objects.update_or_create(
                org_id=org_id.id, symbol="BTC", price=btc_price

            )
            models.CryptoPriceModel.objects.update_or_create(
                org_id=org_id.id, symbol="ETH", price=eth_price

            )
        print("Done!")
        return "Crypto prices updated."
    return "Failed to fetch prices."
