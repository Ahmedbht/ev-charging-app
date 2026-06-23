from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests 
import os
from dotenv import load_dotenv
from models import Station, Operator,ConnectionType
from validators import StationValidator
from utils import filter_by_country, filter_operational , sort_by_points ,analyze_stations
import json

#get env file to know the api-key
load_dotenv()
API_KEY = os.getenv("API_KEY")

#create Fast Api app
app =FastAPI()

#contact with react back to front
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#func to get stations from Open Charge Map api
def fetch_stations(country_code="MA", max_results= 100):
    #read data from local json file
    with open("stations_data.json", "r", encoding='utf-8') as f:
        data =json.load(f)
    return data

    #params we sent to API
    params={
        "key": API_KEY,
        "countrycode":country_code,
        "maxresults": max_results,
        "compact": True,
        "verbose": False,
    }

    response = requests.get(url, params=params)
    print (f"RESPONSE STATUS: {response.status_code}")
    #if it go wrong
    if response.status_code !=200:
        raise HTTPException(status_code=500, detail="Failed to fetch stations")
    return response.json()

    #function get raw data from API and convert it to our station objects
def parse_stations(raw_data):
    stations = []
    for item in raw_data:
        try:
            #verify data using pydantic before create stations
            validated = StationValidator(
                id=item.get("ID"),
                name=item.get("AddressInfo",{}).get("Title", "Unknown"),
                city=item.get("AddressInfo",{}).get("Town"),
                country=item.get("AddressInfo",{}).get("Country",{}).get("Title"),
                latitude=item.get("AddressInfo",{}).get("Latitude"),
                longitude=item.get("AddressInfo",{}).get("Longitude"),
                is_operational=item.get("StatusType",{}).get("IsOperational") if item.get("StatusType") else None,
                number_of_points=item.get("NumberOfPoints"),
            )
            #create station objecs
            station= Station(
                id=validated.id,
                name=validated.name,
                city=validated.city,
                country=validated.country,
                latitude=validated.latitude,
                longitude=validated.longitude,
                operator= item.get("OperatorInfo",{}).get("title") if item.get("OperatorInfo") else None,
                connection_types=[],
                is_operational=validated.is_operational,
                number_of_points=validated.number_of_points,
            )

            stations.append(station)
        except Exception as e:
            print(f"skipp station:{e}")
            continue
    return stations

#endpoint to get stations /react contact endpoint to get stations
@app.get("/stations")
def get_stations(country: str= "MA"):
    raw_data =fetch_stations(country_code=country)
    stations= parse_stations(raw_data)

    #list of dictionaries to send to frontend
    return[
        {
            "id": s.id,
            "name": s.name,
            "city": s.city,
            "country": s.country,
            "latitude": s.latitude,
            "longitude": s.longitude,
            "operator": s.operator,
            "is_operational": s.is_operational,
            "number_of_points": s.number_of_points,
        }
        for s in stations
    ]

#endpoint to get operational/operational
@app.get("/stations/operational")
def get_operational_stations(country: str="MA"):
    raw_data=fetch_stations(country_code=country)
    stations= parse_stations(raw_data)
    operational=filter_operational(stations)

    return[
        {
            "id": s.id,
            "name": s.name,
            "city": s.city,
            "is_operational": s.is_operational,
            "number_of_points": s.number_of_points,
        }
        for s in operational
    ]

#endpoint to get stations/analytics
@app.get("/stations/analytics")
def get_analytics(country: str ="MA"):
    raw_data =fetch_stations(country_code =country)
    stations= parse_stations(raw_data)
    analytics= analyze_stations(stations)
    return analytics

#endpoint to get top stations
@app.get("/stations/top")
def get_top_stations(country: str="MA"):
    raw_data =fetch_stations(country_code = country)
    stations= parse_stations(raw_data)
    sorted_stations= sort_by_points(stations)

    #just top 10
    return[
        {
            "id": s.id,
            "name": s.name,
            "city": s.city,
            "number_of_points": s.number_of_points,
        }
        for s in sorted_stations[:10]
    ] 