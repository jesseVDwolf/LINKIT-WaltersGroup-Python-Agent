from fastapi import FastAPI
import uvicorn
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
        liters_needed: List[float] = [
            offer.km_to_deliver / km_per_liter_consumption * diesel_price_per_liter
            for offer in req.offers
        ]

        # FIRST Algorithm
        # find the uid for the offer with the best margin where
        # margin = req.offers[x].price / req.offers[x].eta_to_deliver
        _, offer = max(enumerate(req.offers), key=lambda offer: (offer[1].price - 0)  / offer[1].eta_to_deliver)

        return DecideResponse(command="DELIVER", argument=offer.uid)
    else:
        return DecideResponse(command="SLEEP", argument=1)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
