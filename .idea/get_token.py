import base64
import requests

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
access_token = get_access_token(client_id, client_secret)
print(f'Access Token: {access_token}')