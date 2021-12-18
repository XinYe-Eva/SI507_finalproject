# SI507_finalproject

Welcome to my SI507 final project! This is a project about a guide tour and restaurant advisor application is realized. User could search different types of restaurants recommended in different states and also get the information of nearby places of the restaurant.

# Project Description
First, the user can choose a state in all 52 states we provided. They could also choose whether see the map of this state by clicking on the box.

Secondly, user could see two bar plots which describes the average ratings and prices of 6 types restaurants in this state. User could choose a food type. 

Thirdly, user could see the top 10 restaurant in the food type and state they chose. We also provided two scatter plots which describes the distribution of prices and ratings of these restaurant. 

At last, user could choose the restaurant they have interested in, input its ranking number and get more information about this restaurant such as its phone, address, and information about places of interests nearby.

# Introduction of code
The final_project.py file utilizes flask to display the data.
The cache.json file served as the database and storage the data needed for this project.
The creat_cache_yelp.py file has four parts: accessing needed data from Yelp API, accessing needed data from MapQuest API, organized data into the tree and save them in cache.json file.
The templates folder includes four html template files for interacting.

# Data Structure and How data is organized into data structure 
I use tree as the main data structure.
The creat_yelp_cache.py includes the data of how I access Web API using API key and get the data I needed. At the same time of getting data, I save them and organized them into a tree structure json file cache_yelp.json which serves as the main database of this project.

# How to running the code
# Step1: Get your API keys and put them in secrets.py
In order to run the code, you need to get your own API keys from YELP and MapQuest.

The website for you to get YELP API Key: https://www.yelp.com/developers/documentation/v3/authentication
(click “Go to Create App, follow their instructions and get your API key!)
The website for you to get MapQuest API Key: https://developer.mapquest.com (click “Get your free API Key”). 

Once you get API keys, make secrets.py in the same folder with your project code and save the API key in secrets.py.  The secrets.py file should contain two single line like this (replace “xxxxxxx” with your API key): 
YELP_API_KEY = xxxxxxx
MAPQUEST_API_KEY = xxxxxxx
# Step2: Install Python Packages
Please install the Python packages for my project to work first:

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

from bs4 import BeautifulSoup

import re
# Step3: Run the final_project.py
This program was made by Flask app, please run the final_project.py locally:
Python final_project.py

Then open http://127.0.0.1:5000/ in your browser.
# Step 4: Interact with the program
After open the http://127.0.0.1:5000/ , you could find an interesting website. You could select the state you want to visit in the box and also choose whether open the map of this state at the same time. Click on “Let’s go!” and you will get to a new page. 

In this new page, you could see two bar plots which describes the average ratings and prices of 6 types restaurants in this state. You could choose a food type you want and click on “Let’s go” and you will get to a new page. To be notice, if you choose open the map at the same time, you will also open a web which contains the map if the state you choose. 

The third page offer you the top 10 restaurant in the food type and state you choose. You could also see two scatter plots which describes the distribution of prices and ratings of these restaurant at the same time. You could choose the restaurant you have interested in, input its number and click on the button to get more information about this restaurant.

At the last page, you could see the details information about this restaurant including its phone and address. We also provide three places of interest nearby this restaurant for you.

If you still have any questions on interacting with the program, here is a demo link!


