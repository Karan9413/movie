# 🎬 Movie Recommendation System

A **content-based Movie Recommendation System** built with **Python**, **Scikit-learn**, and **Streamlit**. The application recommends movies similar to a selected title by analyzing textual features such as genres, keywords, cast, and movie overviews.

---

## 🚀 Features

* 🎯 Select a movie from a dropdown menu.
* 🎬 Get the **Top 5** similar movie recommendations.
* 🧠 Content-based filtering using **Cosine Similarity**.
* ⚡ Fast and interactive web interface built with Streamlit.
* 📊 Powered by the TMDB 5000 Movies dataset.

---

## 🧠 How It Works

The recommendation system follows these steps:

1. Load the TMDB movie and credits datasets.
2. Combine important textual features such as:

   * Genres
   * Keywords
   * Cast
   * Overview
3. Convert the combined text into numerical vectors using **CountVectorizer** or **TF-IDF Vectorizer**.
4. Calculate the similarity between movies using **Cosine Similarity**.
5. When a movie is selected, return the **Top 5** most similar movies.

---

## 🛠️ Tech Stack

* Python
* Pandas
* NumPy
* Scikit-learn
* Streamlit
* Pickle

---

## 📂 Project Structure

```text
movie/
│── app.py
│── movie_recommendation.ipynb
│── tmdb_5000_movies.csv
│── tmdb_5000_credits.csv
│── requirements.txt
│── README.md
│── LICENSE
```

> **Note:** `similarity.pkl` and `movies.pkl` are intentionally **not included** in this repository because it exceeds GitHub's file size limit. they can be generated locally by running the notebook.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Karan9413/movie.git
cd movie
```

### 2. Create a virtual environment

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Generate the model files

Run the notebook to generate the required files:

```bash
pip install notebook
jupyter notebook movie_recommendation.ipynb
```

This creates:

* `movies.pkl`
* `similarity.pkl`

### 5. Run the application

```bash
streamlit run app.py
```

---

## 📊 Dataset

This project uses the **TMDB 5000 Movie Dataset**, including:

* Movie Titles
* Genres
* Keywords
* Cast
* Crew
* Overview

---

## 🔥 Machine Learning Model

* **Recommendation Type:** Content-Based Filtering
* **Feature Engineering:** Combined genres, keywords, cast, and overview
* **Vectorization:** CountVectorizer / TF-IDF
* **Similarity Metric:** Cosine Similarity
* **Output:** Top 5 similar movies

---

## 🚀 Future Improvements

* Display movie posters using the TMDB API.
* Add search functionality.
* Recommend movies by genre.
* Build a hybrid recommendation system.
* Add user ratings and personalized recommendations.
* Deploy the application on Streamlit Community Cloud.

---

## 👨‍💻 Author

**Karan Bhati**

GitHub: https://github.com/Karan9413

---

## ⭐ Support

If you found this project useful, please consider giving it a **⭐ Star** on GitHub. Your support is appreciated!
