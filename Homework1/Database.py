import psycopg2
import BadRequestException
import ConflictException


class Database:
    conn = None
    cursor = None
    database = "postgres"
    host = "localhost"
    user = "postgres"
    password = "POSTGRES"
    port = "5432"

    def __init__(self):
        self.connect()

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database=self.database, host=self.host, user=self.user, password=self.password, port=self.port)
            self.cursor = self.conn.cursor()
            print("Connection successful")
        except psycopg2.Error as e:
            print("Connection failed")
            print(e)

    def get_movies(self, filters=None):
        if filters is None:
            self.cursor.execute("SELECT * FROM movies")
            return self.cursor.fetchall()
        else:
            filters_dict = {}
            if "&" in filters:
                for filter in filters.split("&"):
                    filters_dict[filter.split("=")[0]] = filter.split("=")[1]
            else:
                filters_dict[filters.split("=")[0]] = filters.split("=")[1]
            if "id" in filters_dict:
                self.cursor.execute(
                    f"SELECT * FROM movies WHERE id = {filters_dict['id']}")
                return self.cursor.fetchall()
            elif "maxYear" in filters_dict and "minYear" in filters_dict:
                self.cursor.execute(
                    f"SELECT * FROM movies WHERE year BETWEEN {filters_dict['minYear']} AND {filters_dict['maxYear']}")
                return self.cursor.fetchall()
            elif "maxYear" in filters_dict:
                self.cursor.execute(
                    f"SELECT * FROM movies WHERE year <= {filters_dict['maxYear']}")
                return self.cursor.fetchall()
            elif "minYear" in filters_dict:
                self.cursor.execute(
                    f"SELECT * FROM movies WHERE year >= {filters_dict['minYear']}")
                return self.cursor.fetchall()

    def add_movie(self, title, year, director, rating, id=None):
        if id is None:
            try:
                self.cursor.execute(
                    f"INSERT INTO movies (title, year, director, rating) VALUES ('{title}', {year}, '{director}', {rating})")
            except psycopg2.Error as e:
                print(e)
        else:
            try:
                self.cursor.execute(
                    f"INSERT INTO movies (id, title, year, director, rating) VALUES ({id}, '{title}', {year}, '{director}', {rating})")
            except psycopg2.Error as e:
                print(e)
                raise ConflictException.ConflictException(
                    "ID already exists")
        self.conn.commit()

    def add_movie_json(self, data_json):
        if "title" not in data_json or "year" not in data_json or "director" not in data_json or "rating" not in data_json:
            raise BadRequestException.BadRequestException("Data missing")
        elif "id" in data_json:
            self.add_movie(data_json["title"], data_json["year"],
                           data_json["director"], data_json["rating"], data_json["id"])
        else:
            self.add_movie(data_json["title"], data_json["year"],
                           data_json["director"], data_json["rating"])

    def add_movies(self, movies):
        for movie in movies:
            self.add_movie(movie[0], movie[1], movie[2], movie[3])

    def delete_movie(self, json):
        if "id" in json:
            self.cursor.execute(f"DELETE FROM movies WHERE id = {json['id']}")
        else:
            query = "DELETE FROM movies WHERE "
            if "title" in json:
                query += f"title = '{json['title']}'"
            if "year" in json:
                if "title" in json:
                    query += " AND "
                query += f"year = {json['year']}"
            if "director" in json:
                if "title" in json or "year" in json:
                    query += " AND "
                query += f"director = '{json['director']}'"
            if "rating" in json:
                if "title" in json or "year" in json or "director" in json:
                    query += " AND "
                query += f"rating = {json['rating']}"
            self.cursor.execute(query)
        self.conn.commit()

    def update_movie_json(self, data_json):
        if "id" not in data_json:
            raise BadRequestException.BadRequestException("ID missing")
        id = data_json["id"]
        title = None
        year = None
        director = None
        rating = None
        if "title" in data_json:
            title = data_json["title"]
        if "year" in data_json:
            year = data_json["year"]
        if "director" in data_json:
            director = data_json["director"]
        if "rating" in data_json:
            rating = data_json["rating"]

        self.update_movie(id, title, year, director, rating)

    def update_movie(self, id, title=None, year=None, director=None, rating=None):
        if title is None:
            title = self.get_movie(id)[0][1]
        if year is None:
            year = self.get_movie(id)[0][2]
        if director is None:
            director = self.get_movie(id)[0][3]
        if rating is None:
            rating = self.get_movie(id)[0][4]

        self.cursor.execute(
            f"UPDATE movies SET title = '{title}', year = {year}, director = '{director}', rating = {rating} WHERE id = {id}")
        self.conn.commit()

    def convert_to_json(self, data):
        json = []
        for row in data:
            json.append({
                "id": row[0],
                "title": row[1],
                "year": row[2],
                "director": row[3],
                "rating": row[4]
            })
        return str(json)
