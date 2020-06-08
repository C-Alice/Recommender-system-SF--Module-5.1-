import streamlit as st
import numpy as np
import pandas as pd
import lightfm as lf
import nmslib
import pickle
import scipy.sparse as sparse
import time
import requests
from ast import literal_eval

#@st.cache
def nearest_books_nms(itemid, index, n=10):
    """Function to find nearest neighbours, returns ids of each nearest neighbour"""
    itemid = int(itemid)
    nn = index.knnQuery(item_embeddings[itemid], k=n)
    return nn


def get_files(folder_name='data'):
    """
    Function to read and preprocess files
    """
    items = pd.read_csv(folder_name+'/products.csv')
    items['itemid'] = items['itemid'].astype(str)
    items['image'] = items['image'].apply(lambda x: x[2:-2] if pd.notnull(x) else x)
    items['style'] = items['style'].fillna('No description')
    return items

#@st.cache
def get_embeddings():
    """
    Function to load and prepare embeddings
    """
    with open('item_embeddings_food.pickle', 'rb') as f:
        item_embeddings = pickle.load(f)
    nms_idx = nmslib.init(method='hnsw', space='cosinesimil')
    nms_idx.addDataPointBatch(item_embeddings)
    nms_idx.createIndex(print_progress=True)
    return item_embeddings,nms_idx

def product_description(option):
    """
    Function to create product descriptions
    """
    choice = products[products['itemid'] == option]
    url = choice['image'].iloc[0]
    img = requests.get(url).content
    title = choice['title'].iloc[0].split(',')[0]
    style = choice['style'].iloc[0]
    rating_star = int(choice['overall'].mean())
    return choice, img, title, style, rating_star
    

st.title('Hi and welcome to test our first recommendation engine!')


#load data and embeddings
products  = get_files()  
item_embeddings,nms_idx = get_embeddings()

#insert id or a part of id of a chosen product
product = st.text_input('Search for product...', '')

#search for all the corresponding products in a database
output = products[products['itemid'].str.contains(product) > 0]

#choose a product from a list
option = st.selectbox('Select product', output['itemid'].values)

#print the information about the chosen product
st.header('Product info: ')

choice, img, title, style, rating_star = product_description(option)
st.image(img, width=150)  #image
st.markdown(f'~__*{title}*__~') #product name
if style != 'No description':  #product description
    style = literal_eval(style)
    for key, value in style.items():
        st.markdown(f'*{key}*')
        st.write(value)
else:
    st.text(style)
st.image(['star.png']*rating_star, width=20) #product rating

#customers reviews on the product
if st.button("Show customers' reviews on the product"):
    rev = choice.drop_duplicates('reviewerName')
    for name, summary, review in zip(rev['reviewerName'][:5], rev['summary'][:5], rev['reviewText'][:5]): 
        st.subheader(name)
        st.markdown(f'----*{summary}*----')
        st.write(review)
        st.markdown('------')

#recommendations for the product
st.sidebar.header('Products, you may also like: ')

val_index = output[output['itemid'].values == option]['itemid'].iloc[0]
index = nearest_books_nms(val_index, nms_idx, 5)

#print recommendations along with a brief information about the recommended products
for idx in index[0][1:]:
    try:
        choice, img, title, style, rating_star = product_description(str(idx))
        st.sidebar.image(img, caption=f'Product ID: {idx}') #image
        st.sidebar.markdown(f'~{title}~') #product name
        if style != 'No description':  #product description
            style = literal_eval(style)
            for key, value in style.items():
                st.sidebar.text(key)
                st.sidebar.text(value)
        else:
             st.sidebar.text(style)
        st.sidebar.image(['star.png']*rating_star, width=20) #product rating
        st.sidebar.markdown('-----')
    except:
        st.sidebar.text('')


