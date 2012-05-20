import requests
import json

key = '1fa19d3aecbd7c51be3dd95a122b2ab7'
show = "bleach".replace(' ', '+')

def fetch_url(address):
        r = requests.get(address)
        return json.loads(r.text)

def search_show(show):
    url = 'http://api.trakt.tv/search/shows.json/%s/%s'
    return fetch_url(url % (key, show))

def episode_info(show, season, episode):
    url = 'http://api.trakt.tv/show/episode/summary.json/%s/%s/%i/%i'
    return fetch_url(url % (key, show, season, episode))

def seasons_info(show):
    url = 'http://api.trakt.tv/show/seasons.json/%s/%s'
    return fetch_url(url % (key, show))

def flat_to_season(show, number):
    seasons = {s['season']:s['episodes'] for s in seasons_info(show)}
    if 0 in seasons:
        del seasons[0]
    for s in seasons:
        if number - seasons[s] > 0:
            number -= seasons[s]
        else:
            return (s, number)

proper_name = search_show(show)[0]['title']
print flat_to_season(proper_name.replace(' ', '-'), 72)
