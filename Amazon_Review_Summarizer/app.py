# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 17:52:16 2024

@author: Nithin
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

import streamlit as st
from streamlit_lottie import st_lottie

import os
import google.generativeai as genai


genai.configure(api_key=st.secrets.GEMINI_AI_KEY)

prompt="""You are an online review summarizer who summarizes reviews and makes a small review using all the reviews provided. Please follow the instructions below: 
    1. Summarize the reviews and give a review in a maximum of 200 words,representing all the reviews. 
    2. List the pros and cons as bullet points, with a maximum of 5 points each. 
    3. Give your opinion with a header for each section,
    i.e., 1. Summarized review and review, 2. Pros and cons, 3. My opinion. you can give additional information as well 
    Please note that you should not mention in the output text that you are an AI-powered assistant this is the reviews : 
        """
    


def load_lottieurl(url: str):
    r = requests.get(url)
    return r.json()
feedback = load_lottieurl("https://raw.githubusercontent.com/nithinganesh1/Deployed_Project/main/Flight_Ticket_Price_Prediction/feedback%20Animation.json")
reviewsum = load_lottieurl("https://raw.githubusercontent.com/nithinganesh1/GoogleGemini/main/Amazon_Review_Summarizer/Animation%20-%201708002418746.json")

headers = {
    'authority': 'www.amazon.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

#Get Review Link
#review link
len_page = 4

# Extra Data as Html object from amazon Review page
def reviewsHtml(url, len_page):
    
    # Empty List define to store all pages html data
    soups = []
    
    # Loop for gather all reviews
    for page_no in range(1, len_page + 1):
        
        # parameter set as page no to the requests body
        params = {
            'ie': 'UTF8',
            'reviewerType': 'all_reviews',
            'filterByStar': 'critical',
            'pageNumber': page_no,
        }
        
        # Request make for each page
        response = requests.get(url, headers=headers)
        
        # Save Html object by using BeautifulSoup4 and lxml parser
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Add single Html page data in master soups list
        soups.append(soup)
        
    return soups

# Grab Reviews name, description, date, stars, title from HTML
def getReviews(html_data):

    # Create Empty list to Hold all data
    data_dicts = []
    
    # Select all Reviews BOX html using css selector
    boxes = html_data.select('div[data-hook="review"]')
    
    # Iterate all Reviews BOX 
    for box in boxes:
        
        # Select Name using css selector and cleaning text using strip()
        # If Value is empty define value with 'N/A' for all.
        try:
            name = box.select_one('[class="a-profile-name"]').text.strip()
        except Exception as e:
            name = 'N/A'

        try:
            stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
        except Exception as e:
            stars = 'N/A'   

        try:
            title = box.select_one('[data-hook="review-title"]').text.strip()
        except Exception as e:
            title = 'N/A'

        try:
            # Convert date str to dd/mm/yyy format
            datetime_str = box.select_one('[data-hook="review-date"]').text.strip().split(' on ')[-1]
            date = datetime.strptime(datetime_str, '%B %d, %Y').strftime("%d/%m/%Y")
        except Exception as e:
            date = 'N/A'
        try:
            description = box.select_one('[data-hook="review-body"]').text.strip()
        except Exception as e:
            description = 'N/A'

        # create Dictionary with al review data 
        data_dict = {
            'Name' : name,
            'Stars' : stars,
            'Title' : title,
            'Date' : date,
            'Description' : description
        }

        # Add Dictionary in master empty List
        data_dicts.append(data_dict)
    
    return data_dicts

# Grab all HTML
def Graballhtml(reviews_url):
    html_datas = reviewsHtml(reviews_url, len_page)
    reviews = []
    for html_data in html_datas:
        review = getReviews(html_data)
        
        # add review data in reviews empty list
        reviews += review
    df_reviews = pd.DataFrame(reviews)
    descriptions = df_reviews["Description"].str.cat(sep="\n")
    return descriptions

## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(all_reviews,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+all_reviews)
    return response.text


def main():
    with st.container():
        st.subheader("hii my name is nithin")
        st.title("AI-Powered Amazon Review Summarizer:")
        st.write("This is a learning project uses web scraping and Gemini AI to summarize Amazon reviews")
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with right_column:
            st.header("One simple step.")
            st.write("##")
            st.write(
                """
                - Unlock the Gold in Reviews: AI-Powered Amazon Insights at Your Fingertips
                - Effortless Shopping: Summarize Thousands of Reviews with One Click
                - Cut Through the Noise: Your Personal AI Shopper Powered by Reviews
                - Reviews Made Easy: AI Unveils the True Story Behind Products
    
                Please review my GitHub profile and provide feedback and suggestions.
                """
            )
            st.write("[ GitHub >](https://github.com/nithinganesh1/GoogleGemini/tree/main/Amazon_Review_Summarizer)")
        with left_column:
            st_lottie(reviewsum,speed=1,reverse=False,loop=True,quality="low",height=None,width=400,key=None)
    # Get the input data from the user
    st.write("---")
    st.write("##")
    reviews_url = st.text_input('Paste Amazone Link here')
    st.caption('Click This Button for Summarize')
    if st.button('Summarize'):
        # Make a prediction
        descriptions = Graballhtml(reviews_url)
        
        if descriptions:
            summarise_text = generate_gemini_content(descriptions,prompt)
            st.markdown("## Detailed Notes:")
            st.write(summarise_text)

    
    with st.container():
        st.header("Send feedback")
        st.caption("Please fill out this form and click 'Send.' I will receive your message via email.")
        contact_form = """
        <form action="https://formsubmit.co/nithingganesh1@gmail.com" method="POST">
            <input type="hidden" name="_captcha" value="false"><br><br>
            <input type="text" name="name" placeholder="Your name" required><br><br>
            <input type="email" name="email" placeholder="Your email" required><br><br>
            <textarea name="message" placeholder="Your feedback here" required></textarea><br>
            <button type="submit">Send</button>
        </form>
        """
        left_column, right_column = st.columns((1,1))
        with right_column:
            st.markdown(contact_form, unsafe_allow_html=True)
            st.write("[ GitHub >](https://github.com/nithinganesh1/GoogleGemini/tree/main/Amazon_Review_Summarizer)")
        with left_column:
            st_lottie(feedback,speed=1,reverse=False,loop=True,quality="low",height=None,width=400,key=None)


if __name__ == '__main__':
    main()