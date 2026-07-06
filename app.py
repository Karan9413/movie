import os
import pickle
import random
import streamlit as st

# =========================
# ⚙️ CONFIG & IMAGES
# =========================
st.set_page_config(
    page_title="Netflix AI Pro",
    layout="wide",
    initial_sidebar_state="collapsed",
)

GENRE_IMGS = {
    "action": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?q=80&w=400&h=600&fit=crop",
    "scifi": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=400&h=600&fit=crop",
    "drama": "https://images.unsplash.com/photo-1485846234645-a62644f84728?q=80&w=400&h=600&fit=crop",
    "thriller": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=400&h=600&fit=crop",
    "default": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=400&h=600&fit=crop"
}

HERO_BG = "https://images.unsplash.com/photo-1574267431644-4ed38bc84b4c?q=80&w=1600&h=500&fit=crop"

# =========================
# 🎨 NETFLIX CLEAN THEME (REDUCED VFX)
# =========================
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: #141414 !important;
        color: #E5E5E5 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }}
    
    .hero-container {{
        position: relative;
        background-image: linear-gradient(to bottom, rgba(20,20,20,0.2) 0%, rgba(20,20,20,0.95) 100%), url('{HERO_BG}');
        background-size: cover;
        background-position: center;
        padding: 80px 40px 40px 40px;
        border-radius: 12px;
        margin-bottom: 30px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
    }}
    
    /* TARGET: Streamlit Column Blocks Containing Cards */
    [data-testid="stVerticalBlock"] {{
        transition: transform 0.2s ease-out, box-shadow 0.2s ease-out !important;
        border-radius: 8px;
    }}
    
    /* REDUCED VFX: Minimal lift, zero neon glow panels */
    [data-testid="stVerticalBlock"]:hover {{
        transform: translateY(-4px);
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5);
        z-index: 99;
    }}
    
    .card-meta {{
        padding: 12px;
    }}
    .match-score {{
        color: #46d369;
        font-weight: bold;
        font-size: 14px;
        margin-bottom: 4px;
    }}
    .movie-card-title {{
        font-size: 14px;
        font-weight: 700;
        color: white;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        margin-bottom: 8px;
    }}
    .maturity-rating {{
        border: 1px solid rgba(255,255,255,0.4);
        padding: 1px 4px;
        font-size: 11px;
        border-radius: 3px;
        color: #bcbcbc;
    }}
    
    div.stButton > button {{
        background-color: #E50914 !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        border-radius: 4px !important;
        width: 100% !important;
    }}
    div.stButton > button:hover {{
        background-color: #b80710 !important;
    }}
    
    div[role="dialog"] {{
        background-color: #181818 !important;
        border: 1px solid #333 !important;
        box-shadow: 0 0 40px rgba(0,0,0,0.95) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# 📦 DATA ENGINE
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
movies_path = os.path.join(BASE_DIR, "movies.pkl")
similarity_path = os.path.join(BASE_DIR, "similarity.pkl")

if not os.path.exists(movies_path) or not os.path.exists(similarity_path):
    st.error("Missing vector assets inside the project directory.")
    st.stop()

movies = pickle.load(open(movies_path, "rb"))
similarity = pickle.load(open(similarity_path, "rb"))
movies = movies.reset_index(drop=True)
movie_list = movies["title"].values

def get_poster_url(title):
    # 1. Try fetching the real poster from TMDB API dynamically
    try:
        # Strip trailing year notations like "(2007)" for clean API queries
        clean_title = title.split("(")[0].strip()
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={clean_title}"
        response = requests.get(url, timeout=3).json()
        
        if response.get("results"):
            poster_path = response["results"][0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception:
        pass
    
    # 2. Fallback to your original keyword logic if API fails (No local images used)
    t = title.lower()
    if any(x in t for x in ["dark", "batman", "knight", "kill", "iron", "war", "dead"]):
        return GENRE_IMGS["thriller"]
    if any(x in t for x in ["space", "avatar", "alien", "star", "matrix", "future", "sub"]):
        return GENRE_IMGS["scifi"]
    if any(x in t for x in ["love", "story", "romantic", "dream", "life", "beautiful"]):
        return GENRE_IMGS["drama"]
    return GENRE_IMGS["default"]

def recommend(movie):
    try:
        index = movies[movies["title"] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
        
        results = []
        for i in distances[1:6]:
            m_title = movies.iloc[i[0]].title
            match_pct = int(i[1] * 100)
            if match_pct <= 0 or match_pct > 99:
                match_pct = random.randint(84, 98)
                
            results.append({
                "title": m_title,
                "poster": get_poster_url(m_title),
                "match": match_pct
            })
        return results
    except Exception:
        return []

# =========================
# 🍿 LOOP COMPONENT OVERVIEW
# =========================
@st.dialog("Movie Details", width="large")
def show_movie_popup():
    movie_title = st.session_state["popup_movie"]
    poster = get_poster_url(movie_title)
    
    p_col1, p_col2 = st.columns([1, 2])
    with p_col1:
        st.image(poster, width="stretch")
    with p_col2:
        st.markdown(f"<h1 style='color: white; margin-top:0;'>{movie_title}</h1>", unsafe_allow_html=True)
        st.markdown("<span style='color: #46d369; font-weight: bold;'>98% Match</span> &nbsp;&nbsp;<span class='maturity-rating'>PG-13</span> &nbsp;&nbsp;2h 14m", unsafe_allow_html=True)
        st.write("")
        st.write("Cluster traversal engine is locked. Selecting alternative titles below updates state context variables instantaneously without collapsing the overlay panel window back to home.")
        st.button("🔥 Play Now", key="popup_play")

    st.markdown("---")
    st.markdown("### 🍿 More Like This")
    
    sub_recs = recommend(movie_title)
    if sub_recs:
        p_cols = st.columns(5)
        for idx, item in enumerate(sub_recs):
            with p_cols[idx]:
                st.image(item['poster'], width="stretch")
                st.markdown(
                    f"""
                    <div class="card-meta" style="background-color:#181818; border-radius:0 0 6px 6px; margin-bottom:8px;">
                        <div class="match-score">{item['match']}% Match</div>
                        <div class="movie-card-title" style="font-size:13px;">{item['title']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button("Explore Node", key=f"popup_loop_{idx}", use_container_width=True):
                    st.session_state["popup_movie"] = item['title']
                    st.rerun()

# =========================
# 🎬 MAIN LAYOUT & RUNNER
# =========================
st.markdown(
    f"""
    <div class="hero-container">
        <div class="hero-badge">★ NETFLIX ORIGINAL MATRIX</div>
        <div class="hero-title">Browse Personal<br>Recommendations</div>
    </div>
    """, 
    unsafe_allow_html=True
)

col1, col2 = st.columns([4, 1])
with col1:
    selected_movie = st.selectbox(
        label="Select Target Title",
        options=movie_list,
        label_visibility="collapsed"
    )
with col2:
    btn = st.button("▶ Play Engine", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

if btn:
    st.session_state["active_search"] = selected_movie

if "active_search" in st.session_state:
    recommendations = recommend(st.session_state["active_search"])
    if recommendations:
        st.markdown(
            f"<h3 style='color: white; font-weight: bold; margin-bottom: 20px;'>Because you watched <span style='color: #E50914;'>{st.session_state['active_search']}</span></h3>", 
            unsafe_allow_html=True
        )
        
        cols = st.columns(5)
        for idx, item in enumerate(recommendations):
            with cols[idx]:
                st.image(item['poster'], width="stretch")
                st.markdown(
                    f"""
                    <div class="card-meta" style="background-color:#181818; border-radius:0 0 4px 4px; margin-bottom: 10px;">
                        <div class="match-score">{item['match']}% Match</div>
                        <div style="margin-bottom: 8px; font-size: 12px; color: #a3a3a3;">
                            <span class="maturity-rating">PG-13</span> &nbsp;2h 14m
                        </div>
                        <div class="movie-card-title">{item['title']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                if st.button("🔴 View Details", key=f"main_grid_{idx}", use_container_width=True):
                    st.session_state["popup_movie"] = item['title']

# =========================================================
# ⚡️ CRITICAL STRUCTURAL INTERCEPT LAYER
# =========================================================
if "popup_movie" in st.session_state and st.session_state["popup_movie"] is not None:
    current_popup = st.session_state["popup_movie"]
    show_movie_popup()
    
    if st.session_state["popup_movie"] != current_popup:
        st.rerun()          