EV Charging Station Finder - Backend

A FastAPI backend that fetches real EV charging station data from the Open Charge Map API.
Tech Stack:
-Python
-FastAPI
-Pydantic
-Requests
-Python-dotenv

API Endpoints
-`GET /stations` → get all EV stations
-`GET /stations/analytics` → get analytics and statistics
-`GET /stations/top` → get top 10 stations by charging points
-`GET /stations/operational` → get operational stations only

Live API
https://ev-charging-app-aape.onrender.com/


How to run locally
1.Clone the repo
2.Create virtual environment: `python -m venv venv`
3.Activate: `venv\Scripts\activate`
4.Install dependencies: `pip install -r requirements.txt`
5.Add your API key in `.env` file: `API_KEY=your_key`
6.Run: `uvicorn main:app --reload`