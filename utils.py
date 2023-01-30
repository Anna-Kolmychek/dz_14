import json
import sqlite3


def get_data_from_db(query: str) -> tuple:
    """Получает из БД данные по запросу query"""

    with sqlite3.connect("netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        db_fetch = cursor.fetchall()

    return db_fetch


def convert_db_to_dict(dict_keys, fetch_values):
    """объединяет данные из БД с ключами в словарь"""

    data_in_dict = []
    for fetch_value in fetch_values:
        data_in_dict.append(dict(zip(dict_keys, fetch_value)))

    return data_in_dict


def get_by_title(title: str) -> dict:
    """Получает выборку из БД по указанному названию (title)"""

    query = f"""
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title LIKE '%{title}%'
            ORDER BY release_year DESC
            LIMIT 1
            """

    dict_keys = ("title",
                 "country",
                 "release_year",
                 "genre",
                 "description",
                 )

    dict_values = get_data_from_db(query)

    data_by_title = convert_db_to_dict(dict_keys, dict_values)

    return data_by_title


def get_by_range_release_year(range_min: int, range_max: int) -> list[dict]:
    """Получает выборку из БД по диапазону лет (включительно)"""

    query = f"""
            SELECT title, release_year
            FROM netflix
            WHERE release_year BETWEEN {range_min} AND {range_max}
            LIMIT 100
            """

    dict_keys = ("title",
                 "release_year",
                 )

    fetch_values = get_data_from_db(query)
    data_range_release_year = convert_db_to_dict(dict_keys, fetch_values)

    return data_range_release_year


def get_by_rating(rating: str) -> list[dict]:
    """Получает выборку из БД по рейтингу.
     На вход строка (children ИЛИ family ИЛИ adult)"""
    rating_dict = {"children": ("G"),
                   "family": ("G", "PG", "PG-13"),
                   "adult": ("R", "NC-17"),
                   }

    if rating in rating_dict:
        rating_in_db = rating_dict[rating]
        query = f"""
                SELECT title, rating, description
                FROM netflix
                WHERE rating IN {rating_in_db}
                """

        dict_keys = ("title",
                     "rating",
                     "description",
                     )

        fetch_values = get_data_from_db(query)
        data_by_rating = convert_db_to_dict(dict_keys, fetch_values)
        return data_by_rating
    else:
        return []


def get_by_listed_in(genre: str) -> list[dict]:
    """Получает выборку из БД по жанру (listed_in)"""

    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{genre}%' 
            ORDER BY release_year DESC
            LIMIT 10
            """

    dict_keys = ("title",
                 "description",
                 )

    fetch_values = get_data_from_db(query)
    data_by_listed_in = convert_db_to_dict(dict_keys, fetch_values)

    return data_by_listed_in


def get_actor_list(actor_1: str, actor_2: str) -> list:
    """Получает выборку из БД по двум актерам,
    Возвращает список тех, кто с ними в паре больше 2х раз"""

    query = f"""
            SELECT DISTINCT "cast"
            FROM netflix
            WHERE "cast" LIKE '%{actor_1}%'
            AND "cast" LIKE '%{actor_2}%'
            """

    fetch_values = get_data_from_db(query)

    all_actors = []
    for row in fetch_values:
        all_actors.extend(row[0].split(', '))

    actors_set = set(all_actors)
    actors_set.remove(actor_1)
    actors_set.remove(actor_2)

    actors_list = []
    for actor in actors_set:
        if all_actors.count(actor) > 2:
            actors_list.append(actor)

    return actors_list


def get_by_type_release_year_listed_in(move_type: str, release_year: int, listed_in: str) -> json:
    """Получает выборку из БД по типу, году выпуска, и жанру"""

    query = f"""
            SELECT title, description
            FROM netflix
            WHERE listed_in LIKE '%{listed_in}%'
            AND type = '{move_type}'
            AND release_year = {release_year}
            """

    dict_keys = ("title",
                 "description",
                 )

    fetch_values = get_data_from_db(query)
    result = convert_db_to_dict(dict_keys, fetch_values)

    return json.dumps(result)

