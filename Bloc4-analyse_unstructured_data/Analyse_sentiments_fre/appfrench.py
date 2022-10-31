# import important modules
#pip install streamlit
# import packages
import streamlit as st
import os
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

# text preprocessing modules
from string import punctuation
import pickle
# text preprocessing modules
from nltk.tokenize import word_tokenize

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re  # regular expression
# Download dependency
for dependency in (
        "brown",
        "names",
        "wordnet",
        "averaged_perceptron_tagger",
        "universal_tagset",
):
    nltk.download(dependency)
import nltk
nltk.download('stopwords')
nltk.download('omw-1.4')

import joblib

import warnings

warnings.filterwarnings("ignore")
# seeding
np.random.seed(123)

# load stop words
stop_words = stopwords.words("french")



# function to clean the text
@st.cache
def text_cleaning(text, remove_stop_words=True, lemmatize_words=True):
    # Clean the text, with the option to remove stop_words and to lemmatize word

    # Clean the text
    text = re.sub(r"[^A-Za-z0-9]", " ", text)
    text = re.sub(r"\'s", " ", text)
    text = re.sub(r"http\S+", " link ", text)
    text = re.sub(r"\b\d+(?:\.\d+)?\s+", "", text)  # remove numbers

    # Remove punctuation from text
    text = "".join([c for c in text if c not in punctuation])

    # Optionally, remove stop words
    if remove_stop_words:
        text = text.split()
        text = [w for w in text if not w in stop_words]
        text = " ".join(text)

    # Optionally, shorten words to their stems
    if lemmatize_words:
        text = text.split()
        lemmatizer = WordNetLemmatizer()
        lemmatized_words = [lemmatizer.lemmatize(word) for word in text]
        text = " ".join(lemmatized_words)

    # Return a list of words
    return text


# functon to make prediction
@st.cache
def make_prediction(Description):
    # clearn the data
    clean_review = text_cleaning(Description)

    # load the model and make prediction
    # Reads in saved classification model
    #model = pickle.load(open('sentimentsfrench_model_pipeline.pkl', 'rb'))
    model = joblib.load("sentimentsfrench_model_pipeline.pkl")

    # make prection
    result = model.predict([clean_review])

    # check probabilities
    probas = model.predict_proba([clean_review])
    probability = "{:.2f}".format(float(probas[:, result]))

    return result, probability

# Set the app title
#streamlit run app.py in conda promt
st.title("Analyse des critique de films en français")
st.write("Une application d'apprentissage automatique simple pour prédire le sentiment d'une critique de film")

# Declare a form to receive a movie's review
form = st.form(key="my_form")
review = form.text_input(label="Entrez le texte de votre critique de film en français")
submit = form.form_submit_button(label="Faire des prédictions")

if submit:
    # make prediction from the input text
    result, probability = make_prediction(review)

    # Display results of the NLP task
    st.header("Résultats")

    if int(result) == 1:
        st.write("Ceci est une critique positive avec une probabilité de ", probability)
    else:
        st.write("Ceci est une critique négative avec une probabilité de ", probability)
