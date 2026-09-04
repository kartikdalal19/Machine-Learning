# import requests
# import pandas as pd
# import difflib
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# OMDB_API_KEY = ''  # 🔑 Add your OMDb API Key here

# # ================== Load and Prepare Data ==================

# movies = pd.read_csv('saved_model/movies.csv')
# # movies['combine'] = movies['combine'].fillna('').str.lower()  # Ensure text is clean

# # Vectorize the 'combine' column
# # cv = CountVectorizer(max_features=5000, stop_words='english')
# # vectors = cv.fit_transform(movies['combine']).toarray()
 
# features = ['genres','keywords','tagline','cast','director']
# for features in features:
#   movies[features] = movies[features].fillna('')
# movies['combine'] = movies['genres'] +  movies['keywords'] +  movies['tagline'] +  movies['cast'] +  movies['director']




# cv = TfidfVectorizer()
# vectors = cv.fit_transform(movies['combine'])

# # Compute similarity once
# similarity = cosine_similarity(vectors)

# # ================== Poster Fetching ==================

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

# # ================== Recommendation Function ==================

# def recommend(movie_name):
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
















import os
import re
import difflib
from functools import lru_cache

import pandas as pd
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "saved_model", "movies.csv")
OMDB_API_KEY = os.getenv("OMDB_API_KEY", "").strip()
PLACEHOLDER = "/static/movie_placeholder.jpg"

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(
        f"movies.csv not found at {CSV_PATH}. Put your dataset in saved_model/movies.csv."
    )

movies = pd.read_csv(CSV_PATH)
movies.columns = [str(c).strip() for c in movies.columns]

# Columns used by the original content-based recommender.
FEATURES = ["genres", "keywords", "tagline", "cast", "director"]
for col in FEATURES + ["title", "overview"]:
    if col not in movies.columns:
        movies[col] = ""
    movies[col] = movies[col].fillna("").astype(str)

# Preserve numeric columns when present.
for col in ["revenue", "vote_average", "vote_count", "runtime", "year"]:
    if col in movies.columns:
        movies[col] = pd.to_numeric(movies[col], errors="coerce")

movies["combine"] = movies[FEATURES].agg(" ".join, axis=1)

# Same ML approach as the original project: TF-IDF + cosine similarity.
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
vectors = vectorizer.fit_transform(movies["combine"])
similarity = cosine_similarity(vectors)


def _clean(value):
    if pd.isna(value):
        return ""
    return str(value).strip()


def _split_people(value):
    """Split common cast/director delimiters without breaking names such as DiCaprio."""
    value = _clean(value)
    if not value:
        return []
    parts = re.split(r"\s*\|\s*|\s*;\s*|\s*,\s*", value)
    return [p.strip() for p in parts if p.strip()]


def _split_genres(value):
    value = _clean(value)
    if not value:
        return []
    parts = re.split(r"\s*\|\s*|\s*;\s*|\s*,\s*", value)
    return [p.strip() for p in parts if p.strip()]


def _get_year(row):
    for col in ["year", "release_year", "release date", "release_date"]:
        if col in row.index and _clean(row[col]):
            value = _clean(row[col])
            match = re.search(r"(18|19|20)\d{2}", value)
            if match:
                return match.group(0)
    return "N/A"


def _get_runtime(row):
    for col in ["runtime", "duration"]:
        if col in row.index and _clean(row[col]):
            return _clean(row[col])
    return "N/A"


def _get_rating(row):
    for col in ["vote_average", "rating", "score"]:
        if col in row.index and pd.notna(row[col]):
            try:
                return round(float(row[col]), 1)
            except (TypeError, ValueError):
                pass
    return None


def _get_revenue(row):
    if "revenue" not in row.index or pd.isna(row["revenue"]):
        return 0.0
    try:
        return float(row["revenue"])
    except (TypeError, ValueError):
        return 0.0


def _format_revenue(value):
    value = float(value or 0)
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value > 0:
        return f"${value:,.0f}"
    return "N/A"


@lru_cache(maxsize=512)
def fetch_poster(title):
    """Return an OMDb poster, or the local placeholder if OMDb is unavailable."""
    if not OMDB_API_KEY or not title:
        return PLACEHOLDER

    try:
        response = requests.get(
            "https://www.omdbapi.com/",
            params={"t": title, "apikey": OMDB_API_KEY, "plot": "short"},
            timeout=8,
        )
        response.raise_for_status()
        data = response.json()
        poster = data.get("Poster")
        if data.get("Response") == "True" and poster and poster != "N/A":
            return poster
    except requests.RequestException as exc:
        print(f"OMDb request failed for {title!r}: {exc}")
    except ValueError:
        print(f"OMDb returned invalid JSON for {title!r}")
    except Exception as exc:
        print(f"Poster error for {title!r}: {exc}")

    return PLACEHOLDER


def _movie_dict(row, score=None):
    title = _clean(row.get("title", "Untitled")) or "Untitled"
    genres = _split_genres(row.get("genres", ""))
    cast = _split_people(row.get("cast", ""))
    director = _clean(row.get("director", ""))
    overview = _clean(row.get("overview", "No overview available."))
    rating = _get_rating(row)

    result = {
        "name": title,
        "title": title,
        "poster": fetch_poster(title),
        "overview": overview or "No overview available.",
        "cast": cast[:6],
        "director": director or "Unknown",
        "genres": genres,
        "genre": genres[0] if genres else "Movie",
        "year": _get_year(row),
        "runtime": _get_runtime(row),
        "rating": rating,
        "revenue": _get_revenue(row),
        "revenue_display": _format_revenue(_get_revenue(row)),
    }
    if score is not None:
        result["similarity"] = float(score)
        result["match"] = round(max(0.0, min(100.0, float(score) * 100)), 1)
    return result


def _find_title(movie_name):
    query = _clean(movie_name)
    if not query:
        return None, []

    titles = movies["title"].tolist()
    exact = movies[movies["title"].str.casefold() == query.casefold()]
    if not exact.empty:
        return int(exact.index[0]), [exact.iloc[0]["title"]]

    # Try substring before fuzzy matching.
    contains = movies[movies["title"].str.casefold().str.contains(query.casefold(), regex=False)]
    if not contains.empty:
        return int(contains.index[0]), contains["title"].head(5).tolist()

    matches = difflib.get_close_matches(query, titles, n=5, cutoff=0.45)
    if matches:
        idx = int(movies.index[movies["title"] == matches[0]][0])
        return idx, matches
    return None, []


def search_movies(query, limit=8):
    query = _clean(query)
    if not query:
        return []
    titles = movies["title"].tolist()
    starts = [t for t in titles if t.casefold().startswith(query.casefold())]
    contains = [t for t in titles if query.casefold() in t.casefold() and t not in starts]
    fuzzy = difflib.get_close_matches(query, titles, n=limit, cutoff=0.35)

    ordered = []
    for title in starts + contains + fuzzy:
        if title not in ordered:
            ordered.append(title)
        if len(ordered) >= limit:
            break
    return ordered


def recommend(movie_name, n=8):
    index, suggestions = _find_title(movie_name)
    if index is None:
        return {
            "found": False,
            "query": movie_name,
            "matched_title": None,
            "suggestions": suggestions or search_movies(movie_name, 5),
            "source": None,
            "recommendations": [],
        }

    source_row = movies.loc[index]
    ranked = sorted(
        enumerate(similarity[index]), key=lambda item: item[1], reverse=True
    )

    recommendations = []
    for row_index, score in ranked:
        if row_index == index:
            continue
        row = movies.iloc[row_index]
        recommendations.append(_movie_dict(row, score))
        if len(recommendations) >= n:
            break

    return {
        "found": True,
        "query": movie_name,
        "matched_title": _clean(source_row["title"]),
        "suggestions": suggestions,
        "source": _movie_dict(source_row),
        "recommendations": recommendations,
    }


def recommend_by_genre(genre, n=8):
    genre = _clean(genre)
    if not genre:
        return None
    mask = movies["genres"].str.casefold().str.contains(re.escape(genre.casefold()), regex=True)
    candidates = movies[mask].copy()
    if candidates.empty:
        return None
    if "vote_average" in candidates.columns:
        candidates = candidates.sort_values("vote_average", ascending=False)
    seed = _clean(candidates.iloc[0]["title"])
    return recommend(seed, n=n)


def get_top_grossing(n=10):
    if "revenue" not in movies.columns:
        return []
    top = movies.sort_values("revenue", ascending=False).head(n)
    return [_movie_dict(row) for _, row in top.iterrows()]


def get_top_directors(n=10):
    counts = {}
    for value in movies["director"]:
        for director in _split_people(value):
            counts[director] = counts.get(director, 0) + 1
    return [
        {"name": name, "movie_count": count}
        for name, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]
    ]


def get_top_actors(n=10):
    counts = {}
    for value in movies["cast"]:
        for actor in _split_people(value):
            counts[actor] = counts.get(actor, 0) + 1
    return [
        {"name": name, "movie_count": count}
        for name, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]
    ]


def get_top_rated_movies(n=10):
    if "vote_average" not in movies.columns:
        return []
    top = movies.dropna(subset=["vote_average"]).sort_values("vote_average", ascending=False).head(n)
    return [_movie_dict(row) for _, row in top.iterrows()]


def get_popular_genres(n=10):
    counts = {}
    for value in movies["genres"]:
        for genre in _split_genres(value):
            counts[genre] = counts.get(genre, 0) + 1
    return [
        {"genre": genre, "count": count}
        for genre, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]
    ]


def get_similarity_matrix(movie_name, n=8):
    result = recommend(movie_name, n=n)
    if not result["found"]:
        return result

    rows = []
    source_index, _ = _find_title(result["matched_title"])
    for row_index, score in sorted(
        enumerate(similarity[source_index]), key=lambda item: item[1], reverse=True
    )[: n + 1]:
        rows.append({
            "title": _clean(movies.iloc[row_index]["title"]),
            "score": round(float(score) * 100, 1),
        })
    return {"found": True, "baseline": result["matched_title"], "items": rows}


def get_catalog_stats():
    return {
        "catalog_size": int(len(movies)),
        "feature_count": len(FEATURES),
    }
