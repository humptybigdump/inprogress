# install relevant packages
import os

#os.system("pip install streamlit")
#os.system("pip install pandas")
#os.system("pip install PIL")


# import packages
import streamlit as st
import pandas as pd
from PIL import Image


# configure the main page if you want (this is not necessary)
st.set_page_config(
    menu_items={
        "Get Help": "https://knowyourmeme.com/memes/cat-looks-inside",
        "Report a bug": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "About": "Important dashboard necessary for the future of civilization."
    }
)


# set the title of your main page
st.title("""Pokémon Dashboard.""")



# you can personalize the sidebar
with st.sidebar:
    # you can customize the title
    st.title("If there are other pages, you can access them here.")



# define columns, relative column size and distance between columns
col = st.columns((1, 1), gap = "medium")


# load images (your diagrams etc.)
image_1 = Image.open("graphics/sentiment_level_pos.png")
image_2 = Image.open("graphics/wordcloud.png")



# put something into the first column
with col[0]:
    st.image(image_1)

# put something into the second column
with col[1]:
    st.image(image_2)




