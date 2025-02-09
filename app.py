from flask import Flask, render_template, jsonify, request
import requests
import asyncio
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_USERNAME = os.getenv("MARKER_API_USERNAME")
API_PASSWORD = os.getenv("MARKER_API_PASSWORD")

if not API_USERNAME or not API_PASSWORD:
    raise ValueError("MARKER_API_USERNAME and MARKER_API_PASSWORD environment variables must be set.")

API_BASE_URL_V2 = "https://markerapi.com/api/v2/trademarks"  # Updated base URL

API_ENDPOINTS = {
    "Serial Number Search": {
        "url": "/serialnumber/{serial_number}",
        "params": ["serial_number"],
        "needs_term": True
    },
    "Trademark Search": {
        "url": "/trademark/{search_term}/status/{status}/start/{start}",
        "params": ["search_term", "status", "start"],
        "needs_term": True
    },
    "Description Search": {
        "url": "/description/{search_term}/status/{status}/start/{start}",
        "params": ["search_term", "status", "start"],
        "needs_term": True
    },
    "Owner Search": {
        "url": "/owner/{search_term}/start/{start}",
        "params": ["search_term", "start"],
        "needs_term": True
    },
    "Expiration Search": {
        "url": "/expiring/{expiring}/start/{start}",
        "params": ["expiring", "start"],
        "needs_term": False # Doesn't need a search term
    },
}



async def fetch_data(session, endpoint_name, **kwargs):
    endpoint = API_ENDPOINTS[endpoint_name]
    url = f"{API_BASE_URL_V2}{endpoint['url']}"

    # Replace placeholders in the URL
    for param in endpoint['params']:
        url = url.replace("{" + param + "}", str(kwargs.get(param, ""))) #Provide default value if param not provided


    auth = aiohttp.BasicAuth(API_USERNAME, API_PASSWORD)

    try:
        async with session.get(url, auth=auth) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.text()
                print(f"Error fetching {endpoint_name}: {response.status} - {error_message}")
                return {"error": f"API Error: {response.status} - {error_message}"}

    except aiohttp.ClientError as e:
        print(f"Client Error fetching {endpoint_name}: {e}")
        return {"error": f"Client Error: {e}"}


async def fetch_all_data(search_terms):  # Accept search terms
    async with aiohttp.ClientSession() as session:
        tasks = []
        for endpoint_name, endpoint_data in API_ENDPOINTS.items():
            kwargs = {}
            if endpoint_data["needs_term"]:
               kwargs["search_term"] = search_terms.get(endpoint_name, "") # Get search term or empty string

            # Add other required params
            if endpoint_name == "Trademark Search" or endpoint_name == "Description Search":
                kwargs["status"] = "all" #Default status to all
                kwargs["start"] = 0 # Default start to 0
            elif endpoint_name == "Owner Search":
                kwargs["start"] = 0
            elif endpoint_name == "Expiration Search":
                kwargs["expiring"] = "6 months"
                kwargs["start"] = 0
            elif endpoint_name == "Serial Number Search":
                kwargs["serial_number"] = search_terms.get(endpoint_name, "")
            tasks.append(fetch_data(session, endpoint_name, **kwargs))

        results = await asyncio.gather(*tasks)
        return dict(zip(API_ENDPOINTS.keys(), results))


@app.route("/")
def index():
    return render_template("index.html", endpoints=API_ENDPOINTS)


@app.route("/fetch_api_data", methods=["POST"])
async def fetch_api_data():
    try:
        search_terms = request.form.to_dict() # Get search terms from the form
        data = await fetch_all_data(search_terms)
        return jsonify(data)
    except Exception as e:
        print(f"Error in fetch_api_data route: {e}")
        return jsonify({"error": "An error occurred during API calls."}), 500


if __name__ == "__main__":
    app.run(debug=True)