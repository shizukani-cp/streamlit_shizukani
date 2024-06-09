import requests
from googletrans import Translator

from .error import error

trans = Translator()


def address(*_):
    # print("call address")
    r = requests.get("https://get.geojs.io/v1/ip/geo.json")
    # print("geted request")
    # print(r.text)
    data = r.json()
    # print("generated json")
    """print(data['latitude'])
    print(data['longitude'])
    print(data['country'])
    print(data['region'])
    print(data['city'])"""
    try:
        return f"""{
                trans.translate(data['country'], src='en', dest='ja').text
                }の{
                trans.translate(data['region'], src='en', dest='ja').text
                }の{
                trans.translate(data['city'], src='en', dest='ja').text
                }だが何だ？"""
    except KeyError:
        return error()
