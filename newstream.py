import streamlit as st
import numpy as np
import pandas as pd
import os, urllib, cv2
from model.inference import MyModel



#this creates an instance of the model(look at source file)
model = MyModel()


def main():
    st.title("Feelings Web App - Demo")


    #this saves the user input
    user_input_string = st.text_input("Place String here")
    user_input_feeling = st.text_input("Place feeling here - optional")

    user_input_string = user_input_string.lower().split()
    user_input_feeling = user_input_feeling.lower().split()



    if not user_input_feeling:
        feeling = ''
    else:
        feeling = user_input_feeling[0]


    #this will return the filter of strings that matches the use rinput
    if user_input_string:
        df = None
        try:
            df, utterances = model.subset_search(user_input_string, feeling)
        except:
            st.write('Does not match any data')

        if df is None:
            st.write('Does not match any data')
        else:
            #appends the returns string / painting urls  into an array
            formatted_strings = format_utterances(utterances)
            urls = painting_urls(df)

            #this will go through the returned filtered df and show on webpage with captions
            for url in range(len(urls)):
                image = load_image(urls[url])
                st.image(image.astype(np.uint8))
                st.write(formatted_strings[url])
                st.write('')

def painting_urls(df):
    ret = []
    for x in df['painting']:
        ret.append(x)
    return ret

def format_utterances(phrases):
    ret = []
    for x in phrases:
        ret.append(' '.join(x))
    return ret

#this will help cache images in case image pops up again
@st.cache(show_spinner=False)
def load_image(url):
    with urllib.request.urlopen(url) as response:
        image = np.asarray(bytearray(response.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = image[:, :, [2, 1, 0]] # BGR -> RGB
    return image

@st.cache
def cache_data_frame():
    return model._initialize()



if __name__ == "__main__":
    main()