from fastapi import FastAPI
import uvicorn
from typing import Tuple, List
from .api import *

app = FastAPI()

@app.post("/decide", response_model=DecideResponse)
def decide(req: DecideRequest) -> DecideResponse:
    """
    See https://app.swaggerhub.com/apis-docs/walter-group/walter-group-hackathon-sustainable-logistics/1.0.0 for 
    a detailed description of this endpoint.
    """
    if req.offers:

        # SECOND algorithm
        # req.offers[x].km_to_deliver / km_per_liter_consumption = liters_needed
        # 2.023 * liters_needed = price_for_gas
        diesel_price_per_liter = 2.023
        km_per_liter_consumption = 5.0
        cargo_delivery_time = 5.0
        price_for_fuel: List[float] = [
            offer.km_to_deliver / km_per_liter_consumption * diesel_price_per_liter
            for offer in req.offers
        ]

        def key_func(offer: Tuple[int, CargoOffer]) -> float:
            return (offer[1].price - price_for_fuel[offer[0]])  / (offer[1].eta_to_deliver + cargo_delivery_time)

        # FIRST Algorithm
        # find the uid for the offer with the best margin where
        # margin = req.offers[x].price / req.offers[x].eta_to_deliver
        _, offer = max(enumerate(req.offers), key=key_func)

        return DecideResponse(command="DELIVER", argument=offer.uid)
    else:
        return DecideResponse(command="SLEEP", argument=1)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
