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
        sleep_time = 18.0

        offers = [ {**cargo_offer.dict()} for cargo_offer in req.offers]
        for offer in offers:
            offer['price_for_fuel'] = offer['km_to_deliver'] / km_per_liter_consumption * diesel_price_per_liter
            incident_chance =  (offer['eta_to_deliver'] + req.truck.hours_since_full_rest - sleep_time) / 10
            if incident_chance > 1:
                incident_chance = 1
            elif incident_chance < 0:
                incident_chance = 0
            offer['extra_time'] = incident_chance * 12.0
            offer['gain'] = (offer['price'] - offer['price_for_fuel']) / (offer['eta_to_deliver'] + cargo_delivery_time + offer['extra_time'])

        # FIRST Algorithm
        # find the uid for the offer with the best margin where
        # margin = req.offers[x].price / req.offers[x].eta_to_deliver
        offer = max(offers, key=lambda x: x['gain'])

        if req.truck.hours_since_full_rest > sleep_time:
            return DecideResponse(command="SLEEP", argument=8)

        if offer['gain'] < 0:
            return DecideResponse(command="SLEEP", argument=1)

        return DecideResponse(command="DELIVER", argument=offer['uid'])
    else:
        return DecideResponse(command="SLEEP", argument=1)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
