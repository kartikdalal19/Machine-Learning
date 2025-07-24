# 🎬 Movie Recommendation System

This project is a **content-based movie recommendation system** built using Python, Pandas, and scikit-learn. It takes a movie title as input and returns a list of similar movies based on their content features from a dataset of aroud 3000 movies. A simple Flask web interface is provided to allow users to interact with the system via a browser.

---

## 📌 Features

- Recommend movies based on user input
- Uses content-based filtering (cosine similarity)
- Flask-powered web interface
- Clean UI built with HTML and CSS
- Deployed using local server

---

## 🧠 How It Works

1. The dataset contains movie details like title, genre, overview, keywords, cast, and crew.
2. These features are combined and vectorized using 'TfidfVectorizer`.
3. Cosine similarity is calculated between movie vectors.
4. Based on similarity scores, the top 10 similar movies are recommended.

---
