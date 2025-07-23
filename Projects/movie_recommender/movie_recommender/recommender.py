


# import pandas as pd
# import pickle
# import difflib
# import requests

# OMDB_API_KEY = '6d1765f3'  # Replace with your real key

# def fetch_poster(title):
#     try:
#         # url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
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



# # 📌 Now define recommend
# def recommend(movie_name):
#     movies = pd.read_csv('saved_model/movies.csv')
#     similarity = pickle.load(open('saved_model/similarity.pkl', 'rb'))

#     titles = movies['title'].tolist()
#     matches = difflib.get_close_matches(movie_name, titles)
    
#     if not matches:
#         return [("No match found", "https://via.placeholder.com/300x450.png?text=No+Match")]

#     match = matches[0]
#     index = movies[movies['title'] == match]['index'].values[0]
#     similarity_scores = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

#     recommendations = []
#     for i in similarity_scores[1:10]:
#         title = movies.iloc[i[0]].title
#         poster = fetch_poster(title)  # ✅ This will now be defined
#         recommendations.append((title, poster))
    
#     return recommendations












import requests
import pandas as pd
import pickle
import difflib

OMDB_API_KEY = ''  # 🔑 Add your OMDb API Key here

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


def recommend(movie_name):
    movies = pd.read_csv('saved_model/movies.csv')
    similarity = pickle.load(open('saved_model/similarity.pkl', 'rb'))

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
