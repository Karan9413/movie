import pickle
import streamlit as st
import requests
import pandas as pd

# =========================
# ⚙️ CONFIG
# =========================
st.set_page_config(
    page_title="Movie Recommender Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# 🎨 UI THEME (NETFLIX STYLE)
# =========================
st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b0b0b;
        color: white;
    }

    .title {
        font-size: 55px;
        font-weight: 800;
        text-align: center;
        color: #E50914;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        color: #aaaaaa;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .card {
        background-color: #181818;
        padding: 10px;
        border-radius: 12px;
        transition: 0.3s;
        text-align: center;
    }

    .card:hover {
        transform: scale(1.05);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# 📦 LOAD DATA
# =========================
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

movies = movies.reset_index(drop=True)
movie_list = movies["title"].values


# =========================
# 🌐 POSTER FETCH (SAFE)
# =========================
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        res = requests.get(url, timeout=5)

        if res.status_code != 200:
            return "https://via.placeholder.com/300x450?text=No+Image"

        data = res.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path

        return "https://via.placeholder.com/300x450?text=No+Image"

    except:
        return "https://via.placeholder.com/300x450?text=No+Image"


# =========================
# 🧠 RECOMMENDER ENGINE
# =========================
def recommend(movie):
    try:
        index = movies[movies["title"] == movie].index[0]

        distances = list(enumerate(similarity[index]))
        distances = sorted(distances, key=lambda x: x[1], reverse=True)

        names = []
        posters = []

        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].id
            names.append(movies.iloc[i[0]].title)
            posters.append(fetch_poster(movie_id))

        return names, posters

    except Exception as e:
        return [], []


# =========================
# 🎬 HEADER
# =========================
st.markdown('<div class="title">NETFLIX AI RECOMMENDER</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI-powered movie suggestions based on similarity</div>', unsafe_allow_html=True)

st.markdown("---")


# =========================
# 🎯 INPUT
# =========================
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown("### 🎥 Select Movie")
    selected_movie = st.selectbox("", movie_list)

with col2:
    st.markdown("### ⚡ Action")
    st.write("Click below to generate recommendations")

    btn = st.button("▶ Recommend")


# =========================
# 🎯 OUTPUT
# =========================
if btn:

    names, posters = recommend(selected_movie)

    if len(names) == 0:
        st.error("No recommendations found. Check dataset or similarity matrix.")
    else:
        st.markdown("## 🍿 Top Picks For You")

        cols = st.columns(5)

        for i in range(5):
            with cols[i]:
                st.markdown('<div class="card">', unsafe_allow_html=True)

                st.image(posters[i], use_container_width=True)
                st.markdown(f"**{names[i]}**")

                st.markdown('</div>', unsafe_allow_html=True)