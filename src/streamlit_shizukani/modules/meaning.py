import re

import requests
from bs4 import BeautifulSoup

from .error import error


def meaning(ch, _):
    # print("called meaning")
    try:
        res = requests.get(f"https://kotobank.jp/word/{ch[:-2]}").text
        soup = BeautifulSoup(res, "html.parser")
        description = soup.find("section", class_="description")
        # print(type(description), str(description))
        tag_re = """<("[^"]*"|'[^']*'|[^'">])*>"""
        mea = re.sub(tag_re, "", str(description).replace(" ", ""))
        if mea is None:
            return "何も見つかんなかったぞくそが"
        return f"{mea}だって。※コトバンク情報"
    except Exception as e:
        print(e)
        return error()
