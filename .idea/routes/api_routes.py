from flask import Flask, jsonify, Blueprint, render_template
import requests, base64

api_routes = Blueprint('api_routes',__name__)

def get_access_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization' : 'Basic ' + base64.b64encode(f'{client_id}:{client_secret}'.encode()).decode(),
        'Content-Type' : 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type' : 'client_credentials'
    }

    response = requests.post(url, headers=headers, data = data)
    response_data = response.json()
    return response_data['access_token']

# Replace with your own client ID and secret
client_id = 'fccc49e5859b49e49edeba60a8f3dd7c'
client_secret = '8a1a47c26d3a4c97aae5e444a3e042f5'
ACCESS_TOKEN = get_access_token(client_id, client_secret) # to constantly have updated access code

@api_routes.route('/')
def home_route():
    return render_template('home.html')

@api_routes.route('/about')
def about_route():
    return render_template('about.html')

@api_routes.route('/top-songs', methods = ['GET'])
def fetch_top_songs():
    api_url = 'https://api.spotify.com/v1/playlists/37i9dQZF1DXcBWIGoYBM5M/tracks'
    headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        top_tracks = [{
            'name': item['track']['name'],
            'artist': ', '.join(artist['name'] for artist in item['track']['artists']),
            'album': item['track']['album']['name'],
            'preview_url': item['track']['preview_url']
        } for item in data.get('items', [])]
        return top_tracks, None  # Return data and no error
    except requests.RequestException as e:
        return None, str(e)  # Return no data and the error message


@api_routes.route('/top-stats') # displays the data in the html file
def top_stats_page():
        top_tracks, error = fetch_top_songs() # call the method above to get tracks
        if error:
            return f"Error: {error}", 500
        if top_tracks is None:
            return " No data available", 500
        return render_template("stats.html", tracks = top_tracks)

