from flask import Flask, request, jsonify
import requests
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import random
app = Flask(__name__)
CORS(app)

headers = {
    "X-RapidAPI-Key": "28c6508dc3msh6ce05a979bffb6ap1dcb38jsneb954abd906b",
    "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
}
url = "https://moviesdatabase.p.rapidapi.com/titles"


def convert_to_simpleIMDb(data):
    data = data['results']
    i = 0
    while i < len(data):
        if 'image' in data[i]:
            del data[i]['image']
        if 'principals' in data[i]:
            del data[i]['principals']
        if 'plot' in data[i]:
            del data[i]['plot']
        if 'titleType' in data[i]:
            if data[i]['titleType'] == 'tvSeries':
                del data[i]['nextEpisode']
        if 'akas' in data[i]:
            del data[i]
            i -= 1
        i += 1
    return data


def convert_to_simpleMD(data):
    data = data['results']
    new_data = []
    year = None
    title = None

    for i in range(len(data)):
        if data[i]['releaseDate'] is not None:
            year = data[i]['releaseDate']['year']
        if data[i]['titleText'] is not None:
            title = data[i]['titleText']['text']
        new_data.append({'id': data[i]['id'], 'year': year, 'title': title})
    return new_data


@app.route('/mdapi/', methods=['GET'])
def get_data1():
    try:
        response = requests.request("GET", url, headers=headers).json()
        converted_data = convert_to_simpleMD(response)
        return converted_data, 200
    except:
        return "Error retrieving data from MoviesDatabase", 500


@app.route('/mdapi/<string:name>', methods=['GET'])
def get_data1_by_name(name):
    try:
        querystring = {"exact": "false"}
        url = "https://moviesdatabase.p.rapidapi.com/titles/search/title/" + name
        response = requests.request(
            "GET", url, headers=headers, params=querystring).json()
        converted_data = convert_to_simpleMD(response)
        return converted_data, 200
    except Exception as e:
        print(e)
        return "Error retrieving data from MoviesDatabase", 500


@app.route('/imdbapi/', methods=['GET'])
def get_data2():
    url = "https://imdb8.p.rapidapi.com/title/find"

    headers = {
        "X-RapidAPI-Key": "28c6508dc3msh6ce05a979bffb6ap1dcb38jsneb954abd906b",
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }
    try:
        querystring = {"q": "Movies"}
        response = requests.request(
            "GET", url, headers=headers, params=querystring).json()
        converted_data = convert_to_simpleIMDb(response)
        return converted_data, 200
    except Exception as e:
        print(e)
        return "Error retrieving data from IMDB", 500


@app.route('/imdbapi/<string:name>', methods=['GET'])
def get_data2_by_name(name):
    url = "https://imdb8.p.rapidapi.com/title/find"

    headers = {
        "X-RapidAPI-Key": "28c6508dc3msh6ce05a979bffb6ap1dcb38jsneb954abd906b",
        "X-RapidAPI-Host": "imdb8.p.rapidapi.com"
    }
    try:
        querystring = {"q": name}
        response = requests.request(
            "GET", url, headers=headers, params=querystring).json()
        converted_data = convert_to_simpleIMDb(response)
        return converted_data, 200
    except:
        return "Error retrieving data from IMDB", 500


@app.route('/simpleapi/', methods=['GET'])
def get_data3():
    try:
        response = requests.get("http://localhost:8000/movies")
        print(response.json())
        return response.json(), 200
    except:
        return "Error retrieving data from Simple API", 500


if __name__ == '__main__':
    app.run(debug=True)
