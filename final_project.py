######################################
##### Name: Xin Ye                ####
##### Uniqname: xinye             ####
##### Project: travel guider      ####
##### encoding: utf-8             ####
######################################

#Thanks to professior Bobby's code on slides!
#Thanks to https://plotly.com/python/bubble-charts/
#Thanks to https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py


from os import name
import requests
import json
import webbrowser
import secrets
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go 
import plotly.express as px
import numpy as np
from flask import Flask, render_template, request


#define key from secrets
YELP_API_KEY = secrets.YELP_API_KEY
MAPQUEST_API_KEY = secrets.MAPQUEST_API_KEY

#define base url
YELP_BASEURL = 'https://api.yelp.com/v3/businesses/search'
MAP_BASEURL = "http://www.mapquestapi.com/search/v2/radius"

list_of_restaurant_type = ['American', 'Chinese', 'Korean', 'Japanese', 'Thai', 'Mexican']


########################################
#### Part1: Setting for using Cache 
########################################
CACHE_YELP = 'cache_yelp.json'
CACHE_DICT = {}
NOCACHE_DICT = {}

def open_cache():
    try:
        cache_file = open(CACHE_YELP, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache

########################################
#### Part2: open the map of state 
########################################
def open_state_map(state):
    state_url = CACHE_DICT[state]["image"]
    webbrowser.open_new(state_url)


######################################################
#### Part3: prepare for the list showed on flask
######################################################
def list_of_restaurant_result(state, food_type):
    '''provide the information list of 10 restaurants in a typical state, typical food type.

    Parameters
    ----------
    state: str
        the state user choose
    food_type: str
        the food type user choose

    Returns
    -------
    list_total: list
        the array which contains 10 restaurants' information, for example:[[1,name1,price1,rating1],[2,name2,price2,rating2]]
    '''
    restaurant_list_in_cache = CACHE_DICT[state]["restaurant"][food_type]
    list_total = []
    number = 1
    for item in restaurant_list_in_cache:
        list_item = []
        list_item.append(number)
        list_item.append(item['name'])
        if 'price' in item.keys():
            list_item.append(float(item["price"]))
        else:
            list_item.append(0)
        list_item.append(float(item['rating']))
        list_total.append(list_item)
        number = number+1
    return list_total

def restaurant_info(state, food_type, resnumber):
    '''provide the information of the restaurant user choose.

    Parameters
    ----------
    state: str
        the state user choose
    food_type: str
        the food type user choose
    resnumber:int
        the id number of the restaurant user choose

    Returns
    -------
    list_total: list
        the array which contains the restaurant' information, for example:[name,rating,price,location,phone]
    '''
    restaurant_dic = CACHE_DICT[state]["restaurant"][food_type][resnumber-1]
    resinfo_list = []
    resinfo_list.append(restaurant_dic['name'])
    resinfo_list.append(restaurant_dic['rating'])
    if 'price' in restaurant_dic.keys():
        resinfo_list.append(restaurant_dic['price'])
    else:
        resinfo_list.append("Unknown")
    resinfo_list.append(restaurant_dic['location']["address1"])
    resinfo_list.append(restaurant_dic['location']["city"])
    resinfo_list.append(restaurant_dic['location']["zip_code"])
    resinfo_list.append(restaurant_dic['phone'])
    return [resinfo_list]

def nearby_info(state, food_type, resnumber):
    '''provide the nearby places of interests' information.

    Parameters
    ----------
    state: str
        the state user choose
    food_type: str
        the food type user choose
    resnumber:int
        the id number of the restaurant user choose

    Returns
    -------
    list_total: list
        the array which contains all nearby places' information, for example:[[name1,address1,city1,caterogy1],[name2,address2,city2,caterogy2]]
    '''
    restaurant_list = CACHE_DICT[state]["restaurant"][food_type][resnumber-1]["nearby_places"]
    nearbyinfo_list = []
    for item in restaurant_list:
        nearbyinfo_list_item = []
        nearbyinfo_list_item.append(item["name"])
        nearbyinfo_list_item.append(item["address"])
        nearbyinfo_list_item.append(item["city"])
        nearbyinfo_list_item.append(item["category"])
        nearbyinfo_list.append(nearbyinfo_list_item)
    return nearbyinfo_list 

###############################################################
#### Part4: prepare for the list for plotty showed on flask
###############################################################
def plot1_data(state):
    '''provide list for plot1: 
        graph of average ratings and prices of 6 types restaurants.

    Parameters
    ----------
    state: str
        the state user choose

    Returns
    -------
    list_name: list
        list of name of the restaurant type
    list_rating: list
        list of average ratings of restaurant in different food types
    list_prize: list
        list of average price of restaurant in different food types
    list_color: list
        list of color for every bar
    '''
    list_name = []
    list_rating = []
    list_prize = []
    list_color = []
    
    restaurant_info_list = CACHE_DICT[state]["restaurant"]
    list_of_restaurant_type = ['American', 'Chinese', 'Korean', 'Japanese', 'Thai', 'Mexican']
    for item in list_of_restaurant_type:
        list_tem = restaurant_info_list[item]
        list_name.append(item)
        for i in list_tem:
            list_rating_item = []
            list_prize_item = []
            list_rating_item.append(float(i["rating"]))
            if 'price' in i.keys():
                list_prize_item.append(float(i["price"]))
            else:
                list_prize_item.append(float(0))
            list_rating.append(np.mean(list_rating_item))
            list_prize.append(np.mean(list_prize_item))
    p=120
    for item in list_name:
        list_color.append(p)
        p=p+2
    return list_rating,list_prize, list_color

def ploty2_data(state, food_type):

    list_name = []
    list_rating = []
    list_prize = []
    list_color = []

    restaurant_info_list = CACHE_DICT[state]["restaurant"][food_type]
    for item in restaurant_info_list:
        list_name.append(item["name"])
        list_rating.append(float(item["rating"]))
        if 'price' in item.keys():
            list_prize.append(float(item["price"]))
        else:
            list_prize.append(0)
    p=120
    for item in list_name:
        list_color.append(p)
        p=p+1
    return list_name,list_rating,list_prize,list_color


# Load the cache
CACHE_DICT = open_cache()

##########################
#### Part5: Flask app
##########################

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('page1_allstate.html') # just the static HTML

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    global state
    state = request.form["state"]

    #user could choose whether open the map of state here
    openmap = request.form.get('openmap', False)
    print(openmap)
    if (openmap):
        open_state_map(state)
    
    #making plot1: graph of average ratings and prices of 6 types restaurants.
    list_name = ['American', 'Chinese', 'Korean', 'Japanese', 'Thai', 'Mexican']
    list_rating,list_prize, list_color = plot1_data(state)

    fig = make_subplots(1, 2, subplot_titles=( "The distribution of Ratings" , "The distribution of Prices" ), print_grid=False)
    fig.add_bar(x=list_name, y=list_rating, marker=dict(color=list_color),  name="rating", row=1, col=1)
    fig.add_bar(x=list_name, y=list_prize, marker=dict(color=list_color), name="price", row=1, col=2)

    div1 = fig.to_html(full_html=False)

    return render_template('response.html', state=state, plot_div=div1)

@app.route('/handle_form2', methods=['POST'])
def handle_the_form2():
    global food_type
    food_type = request.form["food"]
    results = list_of_restaurant_result(state, food_type)

    list_name = ['American', 'Chinese', 'Korean', 'Japanese', 'Thai', 'Mexican']

    list_name,list_rating,list_prize,list_color = ploty2_data(state, food_type)
    fig = make_subplots(1, 2, subplot_titles=( "The distribution of Ratings" , "The distribution of Prices" ), print_grid=False)
    fig.add_scatter(x=list_name, y=list_rating, marker=dict(color=list_color, size = 20),  name="rating", row=1, col=1)
    fig.add_scatter(x=list_name, y=list_prize, marker=dict(color=list_color, size = 20), name="price", row=1, col=2)
    div = fig.to_html(full_html=False)
    return render_template('page3_restaurant.html',
        results=results,
        food=food_type,
        plot_div=div)

@app.route('/handle_form3', methods=['POST'])
def handle_the_form3():
    global resname
    resname = request.form["resname" ]
    resname = int(resname)
    results = restaurant_info(state, food_type, resname)
    results2 = nearby_info(state, food_type, resname)

    return render_template('page4.html',
        results=results,
        results2 = results2)

if __name__ == "__main__":
    app.run(debug=True) 
    
