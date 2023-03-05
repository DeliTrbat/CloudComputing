import Database


class Controller:
    @staticmethod
    def generate_list(filters=None):
        db = Database.Database()
        movies = db.get_movies(filters)
        return db.convert_to_json(movies)

    @staticmethod
    def add_movie(json):
        db = Database.Database()
        db.add_movie_json(json)

    @staticmethod
    def delete_movie(json):
        db = Database.Database()
        db.delete_movie(json)

    @staticmethod
    def update_movie(json):
        db = Database.Database()
        db.update_movie_json(json)
