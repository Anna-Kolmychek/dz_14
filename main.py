from flask import Flask, jsonify
import utils

app = Flask(__name__)

# вьюшка поиска по названию
@app.route('/movie/<title>')
def search_by_title(title: str):
    result = utils.get_by_title(title)
    return result


# вьюшка поиска по диапазону лет
@app.route("/movie/<int:range_min>/to/<int:range_max>")
def search_by_range_release_year(range_min, range_max):
    result = utils.get_by_range_release_year(range_min, range_max)
    return result


# вьюшка поиска по рейтингу
@app.route('/rating/<rating>')
def search_by_rating(rating: str):
    result = utils.get_by_rating(rating)
    return result


# вьюшка поиска по жанру
@app.route('/genre/<genre>')
def search_by_genre(genre: str):
    result = utils.get_by_listed_in(genre)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
