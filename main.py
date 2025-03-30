import requests
import os
from dotenv import load_dotenv
import time
import functions
import pandas

#INSERT STATE AND BUSINESS NAME
STATE="Illinois"
BUSINESS="Truck repair"


load_dotenv()
API_KEY=os.getenv("PLACES_API_KEY")

URL = f"https://maps.googleapis.com/maps/api/place/textsearch/json"

results=[]

company_city=[]
company_name=[]
company_web_url=[]
company_phone_num=[]
company_email=[]
company_has_form=[]


cities=functions.get_cities(STATE)

for city in cities[:1]:
    QUERY=city+" "+BUSINESS
    params = {
        "query": QUERY,
        "key": API_KEY,
    }

    response=requests.get(url=URL,params=params)
    data=response.json()

    while True:
        for item in data["results"]:
            if item not in results:
                company_city.append(city)
                results.append(item)

        next_page_token=data.get("next_page_token")

        if next_page_token:
            params["pagetoken"] = next_page_token
            time.sleep(2)
            response = requests.get(URL, params=params)
            data = response.json()
        else:
            break

for result in results[:5]:
    company_name.append(result["name"])

    place_id=result["place_id"]
    details_url=f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=formatted_phone_number,website&key={API_KEY}"
    details_response=requests.get(details_url)
    details_data=details_response.json()

    web_url=details_data["result"].get("website","Couldn't find website")
    company_web_url.append(web_url)

    phone=details_data["result"].get("formatted_phone_number","Couldn't find phone number")
    company_phone_num.append(phone)

    email=functions.get_email(web_url)
    company_email.append(email)

table={
    # "City":company_city,
    "Name":company_name,
    "Website":company_web_url,
    "Phone number":company_phone_num,
    "Email":company_email,
}

data_table=pandas.DataFrame(table)
data_table.to_csv(f"{STATE} {BUSINESS}.csv",index=False)
