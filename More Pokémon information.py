# load packages
import streamlit as st
from PIL import Image

# title
st.title("More Pokémon information")

# set name of the page in the sidebar
st.sidebar.title("Important information")

# load image
image_1 = Image.open("graphics/wordcloud_2.png")

# post the image
st.image(image_1)

# 5 columns, the third columns is 2 times as big as the other ones
cols = st.columns((1, 1, 2, 1, 1), gap = "medium")

# this way you can place a smaller image in the middle
with cols[2]:
    st.image(image_1)
