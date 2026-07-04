import streamlit as st
import pickle
import pandas as pd

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("🎬 Movie Recommender System")

movie_list = movies['title'].values

option = st.selectbox(
    'Select a movie',
    movie_list
)

def recommend(movie, movies, similarity):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movie_list_sorted = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movies = []
    for i in movie_list_sorted[1:6]:
        movie_id=i[0]

        recommended_movies.append(movies.iloc[i[0]].title)

    return recommended_movies


# button
if st.button('Recommend'):
    results = recommend(option, movies, similarity)
    st.write("### Recommended Movies:")
    for r in results:
        st.write(r)