import requests
import json

def get_trending_movie_ids():
    url = "https://api.themoviedb.org/3/trending/all/day?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZTQ1ZTNhZWU5OTUyMGUwMDM3N2M0OTY1OWNlN2YzMyIsInN1YiI6IjY0NTdkNzRmNmFhOGUwMDExY2EwODQxOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.C2BldSLhHvBbNHgZNTnBiv85oIXwu-Z6T9FC6SKb74k"
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    
    movie_ids = []
    for movie in data['results'][:8]:
        movie_ids.append(movie['id'])

    return movie_ids

def getmovieposter(movie_id):
    
    url = "https://api.themoviedb.org/3/trending/all/day?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZTQ1ZTNhZWU5OTUyMGUwMDM3N2M0OTY1OWNlN2YzMyIsInN1YiI6IjY0NTdkNzRmNmFhOGUwMDExY2EwODQxOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.C2BldSLhHvBbNHgZNTnBiv85oIXwu-Z6T9FC6SKb74k"
    }

    response = requests.get(url, headers=headers)       
    response = response.content
    data = json.loads(response)


    for movie in data['results']: 
        if movie["id"] == movie_id:
            poster_path = movie['poster_path']

    base_url = "https://image.tmdb.org/t/p/original"
    poster_url = base_url + poster_path
    return poster_url



def get_movie_details(movie_id):
    api_key = 'ae45e3aee99520e00377c49659ce7f33'  
    api_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'

    try:
        # Make the API request
        response = requests.get(api_url)
        if response.status_code == 200:
            movie_data = response.json()
            return movie_data
        else:
            return {}
    except requests.RequestException:
        return {}
    

def get_movie_id_by_name(movie_name):
    movie_name = movie_name.replace('_', '+') 
    search_url = f'https://api.themoviedb.org/3/search/movie?query={movie_name}&api_key=ae45e3aee99520e00377c49659ce7f33'


    try:
        # Make the API request for searching the movie
        response = requests.get(search_url)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            if results:
                # Return the first movie ID found in the search results
                return results[0]['id']
            else:
                return None
        else:
            return None
    except requests.RequestException:
        return None
    
def get_movie_backdrop(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/images"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJhZTQ1ZTNhZWU5OTUyMGUwMDM3N2M0OTY1OWNlN2YzMyIsInN1YiI6IjY0NTdkNzRmNmFhOGUwMDExY2EwODQxOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.C2BldSLhHvBbNHgZNTnBiv85oIXwu-Z6T9FC6SKb74k"
    }

    response = requests.get(url, headers=headers)

    # Check if the API call was successful (status code 200)
    if response.status_code == 200:
        backdrop_data = response.json()
        backdrop_images = backdrop_data.get("backdrops", [])
        base_url = "https://image.tmdb.org/t/p/original/"

        if backdrop_images:
            first_backdrop = backdrop_images[1]
            backdrop_url = base_url + first_backdrop["file_path"]
            return backdrop_url

    return None