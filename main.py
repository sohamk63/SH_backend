import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load from Railway environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
CLIENT_ID = int(os.getenv("CLIENT_ID", 100))  # Default 100 if not set

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

# Add Uvicorn server startup if running directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
