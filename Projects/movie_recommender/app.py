# from flask import Flask, request, render_template
# from recommender import recommend

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index2.html')

# @app.route('/recommend', methods=['POST'])
# def recommend_route():
#     movie = request.form['movie']
#     results = recommend(movie)
#     return render_template('result.html', movie=movie, recommendations=results)

# if __name__ == '__main__':
#     app.run(debug=True)







from flask import Flask, jsonify, redirect, render_template, request, url_for

from recommender import (
    get_catalog_stats,
    get_popular_genres,
    get_similarity_matrix,
    get_top_actors,
    get_top_directors,
    get_top_grossing,
    get_top_rated_movies,
    recommend,
    recommend_by_genre,
    search_movies,
)

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.route("/")
def home():
    return render_template(
        "home.html",
        top_grossing=get_top_grossing(10),
        top_rated=get_top_rated_movies(10),
        top_directors=get_top_directors(10),
        top_actors=get_top_actors(10),
        genres=get_popular_genres(10),
        stats=get_catalog_stats(),
    )


@app.route("/recommend", methods=["POST"])
def recommend_route():
    movie = request.form.get("movie", "").strip()
    if not movie:
        return redirect(url_for("home"))

    result = recommend(movie, n=8)
    return render_template("recommendation.html", **result)


@app.route("/genre/<path:genre>")
def genre_route(genre):
    result = recommend_by_genre(genre, n=8)
    if result is None:
        return redirect(url_for("home"))
    return render_template("recommendation.html", **result, genre_seed=genre)


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    return jsonify({"query": query, "results": search_movies(query, 8)})


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    data = request.get_json(silent=True) or {}
    movie = str(data.get("movie", "")).strip()
    if not movie:
        return jsonify({"error": "Movie title is required."}), 400
    return jsonify(recommend(movie, n=8))


@app.route("/api/similarity")
def api_similarity():
    movie = request.args.get("movie", "").strip()
    if not movie:
        return jsonify({"error": "Movie title is required."}), 400
    result = get_similarity_matrix(movie, n=8)
    if not result.get("found"):
        return jsonify(result), 404
    return jsonify(result)


@app.errorhandler(404)
def not_found(_error):
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run()
