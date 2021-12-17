# encoding: utf-8
######################################
##### Name: Xin Ye                ####
##### Uniqname: xinye             ####
##### Project: travel guider      ####
######################################
#Thanks to professior's code on slides!
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



###############################################
######### Setting for using Cache #############
###############################################

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


######################################
#####Part1 introduction of state #####
#####                            #####
######################################

#open the map of state
#webbrowser.open_new(country_tract_now)
def open_state_map(state):
    state_url = CACHE_DICT[state]["image"]
    webbrowser.open_new(state_url)


######################################
##### Part2 App Flask            #####
######################################


def list_of_restaurant_result(state, food_type):
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

def plot1_data(state):
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
    #scatter_data = go.Scatter(x=xvals, y=yvals)
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


# Load the cache, save in global variable
CACHE_DICT = open_cache()



######################################
# Part 3 flask
######################################

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('page1_allstate.html') # just the static HTML

@app.route('/handle_form', methods=['POST'])
def handle_the_form():
    global state
    state = request.form["state"]
    #statemap = CACHE_DICT[state]["image"]
    open_state_map(state)
    
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
    
