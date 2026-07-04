import pickle
import streamlit as st
import requests
import pandas as pd

# Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = movies.reset_index(drop=True)

# Poster fetch
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return ""

        data = response.json()
        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

        return ""

    except:
        return ""

# Recommendation
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    names = []
    posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id   # ✅ FIXED HERE
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))

    return names, posters


# UI
st.header("🎬 Movie Recommender System")

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)

if st.button("Show Recommendation"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])