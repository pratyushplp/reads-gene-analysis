#@title Run this cell to load yours Model
from turtle import onclick
import spacy
import pandas as pd
from PIL import Image
import streamlit as st 
import webbrowser
from elasticsearch import Elasticsearch
# Load this package
prdnlp = spacy.load("en_xner_package")
es = Elasticsearch('https://py_adapter:dzvW8b67B2LnNT@elastic.readstech.com')

# Get the abstrac
params = st.experimental_get_query_params()
src = es.get(index=params['section'], id=params['uuid'])['_source']['description']

# Run and enter your text
#f = open('paper_test.txt','r')
#input_text = f.read()
doc = prdnlp(src)
gene_list = []
label_list = []
for ent in doc.ents:
  gene_list.append(ent.text)
  label_list.append(ent.label_)

img = Image.open("images/navigation_sprite1.png")
string_db_url = "https://string-db.org/api/image/network?identifiers=" + "%0d".join(list(set(gene_list))) + "&add_color_nodes=10&network_type=physical"

### MAIN FUNCTION ###
def main(title = "Gene Analysis App".upper()):
    st.markdown("<h1 style='text-align: center; font-size: 65px; color: #4682B4;'>{}</h1>".format(title), 
    unsafe_allow_html=True)
    st.image("./images/Clara-Parabricks-featured.png")
    df = pd.DataFrame({"Gene":gene_list}).value_counts()
    if len(df.index) > 0:
      st.dataframe(df.reset_index().rename(columns={'index':'Gene', 0:'Count'}))
      st.image("./images/navigation_sprite1.png")
      html_string = "<a href='" + string_db_url + "'>String DB</a>"
      st.markdown(html_string, unsafe_allow_html=True)
    else:
      st.error("Model not found any gene in publication metadata")
      st.markdown('<h4>Publication Metadata</h4>', unsafe_allow_html=True)
      st.markdown(src, unsafe_allow_html=True)
    

if __name__ == "__main__":
    main()