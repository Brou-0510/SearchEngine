"""
This project aims to build a basic search engine including different fundamental components we
talked about them for building up Indexing and Query Processing pipelines. The search engine starts from
command line using “python searchengine.py”. Then, the script shows following options, and the user
selects an option for doing related task.

1- Collect new documents.
2- Index documents.
3- Search for a query.
4- Train ML classifier.
5- Predict a link.
6- Your story!
7- Exit

"""


#Imports
import sys
import os
import time
import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import hashlib
import msvcrt
import datetime
import requests
#pip install bs4
from bs4 import BeautifulSoup
#pip install justext
from justext import justext
#pip install trafilatura
from trafilatura import extract

#Constants
TOPICS = ['Technology', 'Health', 'Entertainment']
STORYFILENAME = "story.txt"
INVERTEDINDEXFILENAME = "invertedindex.txt"

#Global Variables
optionSelected = 1
optionValid = False

# Check that a valid option was entered
def UserOption():
    global optionSelected, optionValid

    # If option is non numeric or less than 1 or greater than 7 
    if optionSelected.isnumeric() == False or int(optionSelected) < 1 or int(optionSelected) > 7:
        print("Error in option entered, ensure that the format follows:\npython searchengine.py \'1-7\'\n\nOptions:\n1- Collect new documents.\n2- Index documents.\n3- Search for a query.\n4- Train ML classifier.\n5- Predict a link.\n6- Your story!\n7- Exit")

    # Else valid input is entered
    else:
        optionSelected = int(optionSelected)
        optionValid = True

# Collect documents from source links file
def collect_documents():
    print("Collecting Documents...\nIf being run for the first time expect collection time of 1 Hour.")
    global TOPICS

    # Create data directory if it doesn't exist
    if not os.path.exists("data"):
        os.mkdir("data")
    
    # Create subdirectories for each topic if they don't exist
    for topic in TOPICS:
        if not os.path.exists("data/" + topic):
            os.mkdir("data/" + topic)

    max_depth = 1
    
    # Read from sources.txt
    with open('sources.txt', 'r') as f:
        for line in f:
            
            # Split line into topic and link
            topic, link = line.strip().split(',')
            
            # Hash URL
            url_hash = hashlib.md5(link.encode('utf-8')).hexdigest()
            
            # Check if page has already been crawled
            if os.path.exists(f'data/{topic}/{url_hash}.txt'):
                continue
           
            # Crawl page
            try:
                crawl_link(link, topic, max_depth, url_hash)

            except requests.exceptions.RequestException:
                pass

# Crawl through the link, collect contents, and save contents to hashed url file
def crawl_link(link, topic, max_depth, url_hash):
    response = requests.get(link)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract content
    text = extract(response.content)
    
    # Remove stopwords from content
    stop_words = set(stopwords.words('english'))
    text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
    
    # Save page content in topic related subfolder
    with open(f'data/{topic}/{url_hash}.txt', 'w', encoding='utf-8') as f:
        f.write(text)
    
    
    # Write to crawl.log file
    with open('crawl.log', 'a') as f:
        f.write(f'{topic}, {link}, {url_hash}, {datetime.datetime.now()}\n')
    
    # Crawl links on page up to a maximum depth
    if max_depth > 0:
        for links in soup.find_all('a'):
            href = links.get('href')
            
            linkParts = link.split("/")
            linkStart = "https://"+ linkParts[2]

            # Check if link exist and if it has intial link in it
            if href is not None and href.startswith(linkStart):
                # Hash URL
                link_hash = hashlib.md5(href.encode('utf-8')).hexdigest()
                
                # Check if link has already been crawled
                if not os.path.exists(f'data/{topic}/{link_hash}.txt'):
                    
                    # Crawl link
                    try:
                        response = requests.get(href)
                        response.raise_for_status()
                        
                        # Extract content
                        text = extract(response.content)
                        
                        if text is not None:

                            # Remove stopwords from content
                            text = ' '.join([word for word in text.split() if word.lower() not in stop_words])
                            
                            # Save page content in topic related subfolder
                            with open(f'data/{topic}/{link_hash}.txt', 'w', encoding='utf-8') as f:
                                f.write(text)
                            
                            # Write to crawl.log file
                            with open('crawl.log', 'a') as f:
                                f.write(f'{topic}, {href}, {link_hash}, {datetime.datetime.now()}\n')
                            
                            # Recursively crawl links up to max_depth
                            if max_depth > 1:
                                crawl_link(href, topic, max_depth-1, link_hash)

                    except requests.exceptions.RequestException:
                        pass
                    except:
                        pass

# Create inverted index using downloaded page and save it as invertedindex.txt
def index_documents():
    file = open(INVERTEDINDEXFILENAME, "w", encoding="utf-8")
    file.write("| Term | Soundex | Appearances (DocHash, Frequency) |\n|------|---------|----------------------------------|")
    

def search_query():
    print("Searching for a query...")
    # code to search for a query goes here

def train_classifier():
    print("Training ML classifier...")
    # code to train ML classifier goes here

def predict_link():
    print("Predicting a link...")
    # code to predict a link goes here

def user_story():

    # Clear screen
    os.system('clear')
    # Save page content in topic related subfolder
    with open(STORYFILENAME, 'r', encoding='utf-8') as f:
        for line in f:
            print(line, end="")


# Run program main
def run():
    global optionSelected, optionValid
    while optionSelected != 7:

        # Clear screen
        os.system('clear')
        
        # Ask user for option
        optionSelected = input("Options:\n1- Collect new documents.\n2- Index documents.\n3- Search for a query.\n4- Train ML classifier.\n5- Predict a link.\n6- Your story!\n7- Exit\n\nEnter your choice: ")

        # Check option selected
        UserOption()

        # If option enter valid
        if optionValid == True:

            # Collect new documents selected
            if optionSelected == 1:
                collect_documents()
                print("\nCollection complete.\nPress any key to return to options menu...")
                msvcrt.getch()

            # Index documents selected
            elif optionSelected == 2:
                index_documents()
                print("\nPress any key to return to options menu...")
                msvcrt.getch()

            # Search for a query selected
            elif optionSelected == 3:
                search_query()
                print("\nPress any key to return to options menu...")
                msvcrt.getch()

            # Train ML classifer selected
            elif optionSelected == 4:
                train_classifier()
                print("\nPress any key to return to options menu...")
                msvcrt.getch()

            # Predict a link selected
            elif optionSelected == 5:
                predict_link()
                print("\nPress any key to return to options menu...")
                msvcrt.getch()

            # Story option selected
            elif optionSelected == 6:
                user_story()
                print("\nPress any key to return to options menu...")
                msvcrt.getch()

            # Exit option selected
            elif optionSelected == 7:
                print("Exiting...")
                



if __name__ == '__main__':
    run()