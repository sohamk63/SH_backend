from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_BASE_URL = "https://api.recruitment.shq.nz"
API_KEY = "h523hDtETbkJ3nSJL323hjYLXbCyDaRZ"
CLIENT_ID = 100


def get_domains(client_id):
    url = f"{API_BASE_URL}/domains/{client_id}?api_key={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_dns_records(zone_id):
    url = f"{API_BASE_URL}/zones/{zone_id}?api_key={API_KEY}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


@app.get("/dns-data")
def dns_data():
    output = []
    domains_data = get_domains(CLIENT_ID)

    for domain in domains_data:
        domain_info = {
            "domain": domain.get("name"),
            "zones": []
        }

        for zone in domain.get("zones", []):
            zone_uri = zone.get("uri")
            zone_id = zone_uri.split("/")[-1]
            records = get_dns_records(zone_id)

            domain_info["zones"].append({
                "zone_id": zone_id,
                "records": records.get("records", [])
            })

        output.append(domain_info)

    return JSONResponse(content=output)
