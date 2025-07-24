# import requests
# import pandas as pd
# import pickle
# import difflib


# def fetch_poster(title):
#     try:
#         url = f"http://www.omdbapi.com/?t={title.strip()}&apikey={OMDB_API_KEY}"
#         response = requests.get(url, timeout=15)
#         data = response.json()
#         if data.get('Response') == 'True':
#             return data.get('Poster') or "https://via.placeholder.com/300x450.png?text=No+Poster"
#         else:
#             print(f"No result for: {title}")
#     except requests.exceptions.ConnectTimeout:
#         print(f"Timeout when connecting to OMDb for movie: {title}")
#     except Exception as e:
#         print(f"Error fetching poster for '{title}':", e)

#     return "https://via.placeholder.com/300x450.png?text=No+Poster"


# def recommend(movie_name):
#     movies = pd.read_csv('saved_model/movies.csv')
#     similarity = pickle.load(open('saved_model/similarity.pkl', 'rb'))

#     titles = movies['title'].tolist()
#     matches = difflib.get_close_matches(movie_name, titles)

#     if not matches:
#         return [{
#             'name': "No match found",
#             'poster': "https://via.placeholder.com/300x450.png?text=No+Match",
#             'overview': "N/A",
#             'cast': "N/A"
#         }]

#     match = matches[0]
#     index = movies[movies['title'] == match]['index'].values[0]
#     similarity_scores = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

#     recommendations = []
#     for i in similarity_scores[1:10]:
#         movie_data = movies.iloc[i[0]]
#         title = movie_data.title
#         overview = movie_data.overview
#         cast = movie_data.cast
#         poster = fetch_poster(title)
        
#         recommendations.append({
#             'name': title,
#             'poster': poster,
#             'overview': overview,
#             'cast': cast
#         })

#     return recommendations









import requests
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# OMDB_API_KEY = ''  # 🔑 Add your OMDb API Key here
OMDB_API_KEY = '6d1765f3'  # 🔑 Add your OMDb API Key here

# ================== Load and Prepare Data ==================

movies = pd.read_csv('saved_model/movies.csv')
# movies['combine'] = movies['combine'].fillna('').str.lower()  # Ensure text is clean

# Vectorize the 'combine' column
# cv = CountVectorizer(max_features=5000, stop_words='english')
# vectors = cv.fit_transform(movies['combine']).toarray()
 
features = ['genres','keywords','tagline','cast','director']
for features in features:
  movies[features] = movies[features].fillna('')
movies['combine'] = movies['genres'] +  movies['keywords'] +  movies['tagline'] +  movies['cast'] +  movies['director']




cv = TfidfVectorizer()
vectors = cv.fit_transform(movies['combine'])

# Compute similarity once
similarity = cosine_similarity(vectors)

# ================== Poster Fetching ==================

def fetch_poster(title):
    try:
        url = f"http://www.omdbapi.com/?t={title.strip()}&apikey={OMDB_API_KEY}"
        response = requests.get(url, timeout=15)
        data = response.json()
        if data.get('Response') == 'True':
            return data.get('Poster') or "https://via.placeholder.com/300x450.png?text=No+Poster"
        else:
            print(f"No result for: {title}")
    except requests.exceptions.ConnectTimeout:
        print(f"Timeout when connecting to OMDb for movie: {title}")
    except Exception as e:
        print(f"Error fetching poster for '{title}':", e)

    return "https://via.placeholder.com/300x450.png?text=No+Poster"

# ================== Recommendation Function ==================

def recommend(movie_name):
    titles = movies['title'].tolist()
    matches = difflib.get_close_matches(movie_name, titles)

    if not matches:
        return [{
            'name': "No match found",
            'poster': "https://via.placeholder.com/300x450.png?text=No+Match",
            'overview': "N/A",
            'cast': "N/A"
        }]

    match = matches[0]
    index = movies[movies['title'] == match]['index'].values[0]
    similarity_scores = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in similarity_scores[1:10]:
        movie_data = movies.iloc[i[0]]
        title = movie_data.title
        overview = movie_data.overview
        cast = movie_data.cast
        poster = fetch_poster(title)

        recommendations.append({
            'name': title,
            'poster': poster,
            'overview': overview,
            'cast': cast
        })

    return recommendations
