from flask import Flask, request, render_template, session, redirect
import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import seaborn as sns
from sklearn import metrics
from sklearn.feature_extraction import text
import nltk
import re
import pickle
import scipy.sparse

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
transform_result = scipy.sparse.load_npz('Y_result.npz')
vectorizer = pickle.load(open("vectorizer.pickle", "rb"))
df_web_extract = pd.read_csv("dict_file.csv")

# df = pd.DataFrame({'A': ['<a href="https://www.unt.edu" target="_blank">https://www.unt.edu</a>', 1, 2, 3, 4, 6],
#                    'B': [5, 6, 7, 8, 9, 10]})


@app.route("/")
def fileFrontPage():
    return render_template('search.html')

@app.route('/handleSearch', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        user_query = request.form['searchtext']
        user_query_vector = vectorizer.transform([user_query])
        results = cosine_similarity(transform_result,user_query_vector).reshape((-1,))
        df = pd.DataFrame(columns = ['Website', 'Website Text'])
        for i in results.argsort()[-10:][::-1]:
            # df = df.append({'Website' : df_web_extract.iloc[i,0], 'Website Text' : df_web_extract.iloc[i,1] }, ignore_index = True)
            df = df.append({'Website' : '<a href=' + df_web_extract.iloc[i,0] + '>' + df_web_extract.iloc[i,0] + '</a>', 
            'Website Text' : df_web_extract.iloc[i,1][:500] }, ignore_index = True)        

         
        return render_template('search.html', tables=[df.to_html(classes='data', index=False, escape=False)], titles=df.columns.values)
    return

# @app.route('/', methods=("POST", "GET"))
# def html_table():
#     return render_template('search.html',  tables=[df.to_html(classes='data', index=False, escape=False)], titles=df.columns.values)