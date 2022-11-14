import requests

from math import sin, cos, sqrt, acos, radians
from services.config import GOOG_KEY, YA_KEY


MAX_DIST = 100

BASE_URL_YA = r'https://geocode-maps.yandex.ru/1.x/'
BASE_URL_YA_2 = 'https://geocode-maps.yandex.ru/1.x?apikey={}&geocode={}&format=json'
BASE_URL_GOOG = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}'

post_data = {}
post_data['apikey'] = YA_KEY

post_data['format'] = 'json'


cnt_adrs = 0


def get_geo_coordinates(adr):
    post_data['geocode'] = adr
    global cnt_adrs
    cnt_adrs += 1
    try:
        r = requests.get(BASE_URL_YA, post_data)
        pos = r.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    except:
        pos = ''
    print(cnt_adrs, '-', adr)
    return pos


def get_geo_coordinates_google(adr):
    pos = ''
    global cnt_adrs
    cnt_adrs += 1
    try:
        r = requests.get(BASE_URL_GOOG.format(adr, GOOG_KEY))
        if r.status_code == 200:
            r = r.json()
            lng = r['results'][0]['geometry']['location']['lng']
            lat = r['results'][0]['geometry']['location']['lat']
            pos = str(round(lat, 6)) + ' ' + str(round(lng, 6))
            print(cnt_adrs, '-', adr)
    except Exception as err:
        print(err)
    return pos


def get_distance_sph(pos0, pos1):
    r = 6371.0
    x1, y1 = pos0.split()
    x2, y2 = pos1.split()
    y1 = radians(float(y1))
    x1 = radians(float(x1))
    y2 = radians(float(y2))
    x2 = radians(float(x2))

    a = sin(y1) * sin(y2) + cos(y1) * cos(y2) * cos(x1 - x2)

    distance = r * acos(a)
    return distance
