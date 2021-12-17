from os import name
from bs4 import BeautifulSoup
import requests
import json
import re
import secrets

YELP_API_KEY = secrets.YELP_API_KEY
MAPQUEST_API_KEY = secrets.MAPQUEST_API_KEY

YELP_BASEURL = 'https://api.yelp.com/v3/businesses/search'
MAP_BASEURL = "http://www.mapquestapi.com/search/v2/radius"

list_of_state = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
#list_of_state = ['Alabama', 'Alaska']
list_of_restaurant_type = ['American', 'Chinese', 'Korean', 'Japanese', 'Thai', 'Mexican']
#list_of_restaurant_type = ['American', 'Chinese']


CACHE_YELP = 'cache_yelp.json'
CACHE_DICT = {}

def open_cache():
    try:
        cache_file = open(CACHE_YELP, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

def save_cache(cache_dict):
    contents_to_write = json.dumps(cache_dict)
    cache_file = open(CACHE_YELP, 'w')
    cache_file.write(contents_to_write)
    cache_file.close()



HEADERS = {'Authorization':  'bearer %s' %YELP_API_KEY}

def scrach_yelp_data(location,  food_category):
    PARAMETERS = {'term': food_category,'location': location, 'limit': 10,' categories': 'restaurants', 'sort_by':'best_match'}

    response = requests.get(url = YELP_BASEURL,params = PARAMETERS,headers = HEADERS)
    json_dict = json.loads(response.text)

    return json_dict['businesses']

def construct_cache_key(location,  food_category):
    yelp_cache_key=location+food_category
    return yelp_cache_key

def recommend_nearby_places(zipcode):
    params = {"origin": zipcode, "radius": 10, "maxMatches": 3, "ambiguities": "ignore", "outFormat":"json", "key": MAPQUEST_API_KEY}
    response = requests.get(MAP_BASEURL , params=params)
    response = json.loads(response.content)
    results_dict_places = []
    if 'searchResults' in response.keys():
        for place in response["searchResults"]:
            result_dict_places = {}
            result_dict_places['name'] = place["fields"]["name"]
            result_dict_places['address'] = place["fields"]["address"]
            result_dict_places['city'] = place["fields"]["city"]
            result_dict_places['category'] = place["fields"]["group_sic_code_name"]  
            
            if not result_dict_places['city']: result_dict_places['city'] = "no city"
            if not result_dict_places['address']: result_dict_places['address'] = "no address"
            if not result_dict_places['category']: result_dict_places['category'] = "no category"
            
            results_dict_places.append(result_dict_places)

    return results_dict_places



#fetch data and put it into tree
dict_all={}
for item in list_of_state:
    dic_allrecord_onestate={}
    #record the image link of this record => node2
    country_image_base = 'https://www.nationsonline.org/maps/USA/Alabama_map.jpg' # 
    country_image=re.sub('Alabama', str(item), country_image_base)
    dic_allrecord_onestate['image'] = country_image

    #record the restaurant of this record => node3
    dic_of_state_res={}
    for food in list_of_restaurant_type:
        result_item_dict = []
        allresult_dict = scrach_yelp_data(item,  food)
        for record in allresult_dict:        
            needresult_dict = {}
            needresult_dict['name'] = record['name']
            needresult_dict['rating'] = record['rating']
            if 'price' in record.keys():
                if record['price'] == '$':
                    needresult_dict['price'] = '1'
                elif record['price'] == '$$':
                    needresult_dict['price'] = '2'
                elif record['price'] == '$$$':
                    needresult_dict['price'] = '3'
                elif record['price'] == '$$$$':
                    needresult_dict['price'] = '4'
                elif record['price'] == '$$$$$':
                    needresult_dict['price'] = '5'
            needresult_dict['location'] = record['location']
            needresult_dict['phone'] = record['phone']

            # search nearby places of intersts of this restaurant and insert the records into the tree!
            needresult_dict['nearby_places'] = recommend_nearby_places(record['location']["zip_code"]) 
            result_item_dict.append(needresult_dict)
        dic_of_state_res[food] = result_item_dict

    dic_allrecord_onestate['restaurant'] = dic_of_state_res
    
    dict_all[item] = dic_allrecord_onestate
save_cache(dict_all) 
            


            


        
