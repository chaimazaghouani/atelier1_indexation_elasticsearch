import io

import streamlit as st
from elasticsearch import Elasticsearch
from PIL import Image

custom_css = """
<style>
    body {
        background-color: #f4f4f4;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }
    .stTextInput input {
        border: 2px solid #0078D4;
        border-radius: 5px;
        padding: 10px;
        width: 100%;
    }
    .stTextInput label {
        color: #0078D4;
        font-weight: bold;
    }
    .stButton button {
        background-color: #0078D4;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .stSuccess {
        color: #0078D4;
        font-weight: bold;
    }
    .stImage img {
        max-width: 100%;
    }
</style>
"""

# Appliquer les styles CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Créer une connexion Elasticsearch
client = Elasticsearch("http://localhost:9200")

# Fonction pour afficher les résultats de la recherche
def display_results(query):
    getreq = {
        "query": {
            "fuzzy": {"tags": query}
        }
    }
    results = client.search(index="flk1", body=getreq)
    cols = st.columns(2)
    col_heights = [0, 0]
    for hit in results["hits"]['hits']:
        image_data = hit["_source"]
        image = "http://farm" + image_data['flickr_farm'] + ".staticflickr.com/" + image_data['flickr_server'] + "/" + image_data["id"] + "_" + image_data['flickr_secret'] + ".jpg"
        col_id = 0 if col_heights[0] <= col_heights[1] else 1
        cols[col_id].image(image)
        col_heights[col_id] += 1

# Partie principale
st.write('## Textual Search Bar')
query = st.text_input('Enter some text')
submit = st.button('Search')
if submit:
    display_results(query)

