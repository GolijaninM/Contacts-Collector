import requests
import os
from dotenv import load_dotenv
import time
import functions
import pandas
import json

#INSERT STATE AND BUSINESS NAME
STATE="State Name"
BUSINESS="Business Name"


load_dotenv()
API_KEY=os.getenv("PLACES_API_KEY")

URL = f"https://maps.googleapis.com/maps/api/place/textsearch/json"
try:
    with open(f"{STATE} ids.json") as file:
        file_data=json.load(file)
        place_ids=file_data["ids"]
except FileNotFoundError:
    place_ids=[]

new_ids=[]
company_city=[]
company_name=[]
company_web_url=[]
company_phone_num=[]
company_email=[]


cities=functions.get_cities(STATE)


for city in cities:
    QUERY=city+" "+BUSINESS
    params = {
        "query": QUERY,
        "key": API_KEY,
    }

    response=requests.get(url=URL,params=params)
    data=response.json()

    while True:
        for item in data["results"]:
            if item["place_id"] not in place_ids:
                company_city.append(city)
                company_name.append(item["name"])
                place_ids.append(item["place_id"])
                new_ids.append(item["place_id"])

        next_page_token=data.get("next_page_token")

        if next_page_token:
            params["pagetoken"] = next_page_token
            time.sleep(2)
            response = requests.get(URL, params=params)
            data = response.json()
        else:
            break

i=1
for id_ in new_ids:
    print(f"{i} / {len(new_ids)}")
    i+=1
    place_id=id_
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
    "City":company_city,
    "Name":company_name,
    "Website":company_web_url,
    "Phone number":company_phone_num,
    "Email":company_email,
}

output_json={
    "ids":place_ids
}

with open(f"{STATE} ids.json","w") as file:
    json.dump(output_json,file)

data_table=pandas.DataFrame(table)
data_table.to_csv(f"{STATE} {BUSINESS}.csv",index=False)
