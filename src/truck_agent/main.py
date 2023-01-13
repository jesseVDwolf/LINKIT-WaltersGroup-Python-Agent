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

        # FIRST Algorithm
        # find the uid for the offer with the best margin where
        # margin = req.offers[x].price / req.offers[x].eta_to_deliver
        offer = max(req.offers, key=lambda offer: offer.price / offer.eta_to_deliver)

        return DecideResponse(command="DELIVER", argument=offer.uid)
    else:
        return DecideResponse(command="SLEEP", argument=1)

def main():
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
