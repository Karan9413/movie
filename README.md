# 🎬 Movie Recommender System (Streamlit)

A content-based movie recommendation system built using Machine Learning and deployed using Streamlit.  
It recommends similar movies based on textual similarity of movie features like genres, keywords, cast, and overview.

---

# 🚀 Live Demo
*(Add your Streamlit Cloud link here after deployment)*

---

# 📌 Features

- 🎯 Select a movie from dropdown
- 🎬 Get top 5 similar movie recommendations
- ⚡ Fast and interactive Streamlit UI
- 🧠 Content-based filtering using cosine similarity
- 📊 Works on TMDB 5000 movie dataset

---

# 🧠 How It Works

The system uses a **content-based recommendation approach**:

1. Movies are converted into feature vectors using text data
2. Similarity between movies is computed using **Cosine Similarity**
3. When a user selects a movie, top similar movies are returned

---

# 🛠️ Tech Stack

- Python 🐍
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Pickle

---

# 📂 Project Structure

```
movie-recommender/
│
├── app.py
├── movies.pkl
├── similarity.pkl (optional / local only)
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── requirements.txt
├── README.md
├── LICENSE
├── movie-recommandastion.ipynb
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the repository

```bash
git clone https://github.com/Karan9413/movie.git
cd movie
```

## 2️⃣ Create virtual environment (optional but recommended)
```
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
```

## 3️⃣ Install dependencies
```
pip install -r requirements.txt
```

## 4️⃣ Run the Streamlit app
```
streamlit run app.py
```

## 📊 Dataset Used
TMDB 5000 Movies Dataset
TMDB 5000 Credits Dataset

## These datasets include:

Movie titles
Genres
Cast
Keywords
Overview

## 🔥 Model Details
Feature Engineering: Combined text features (genres, keywords, cast, overview)
Vectorization: TF-IDF / Count Vectorization
Similarity Metric: Cosine Similarity
Output: Top 5 most similar movies


##👨‍💻 Author
Karan Bhati

⭐ If you like this project

Give it a ⭐ on GitHub and share it!
