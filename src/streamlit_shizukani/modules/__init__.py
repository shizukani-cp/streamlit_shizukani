import datetime
import multiprocessing
import random
import re
import threading
from typing import Callable

import keyboard
import requests
from bs4 import BeautifulSoup
from googletrans import Translator
from janome.tokenizer import Tokenizer

from . import fight

trans = Translator()

week = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]

process = None
shm = None
fight_process = None

tokenizer = Tokenizer()


class Finish:
    def __init__(self):
        pass


class Fight:
    def __init__(self):
        self.speaks = []
        self.p = multiprocessing.Process(target=self.run)
        self.p.start()

    def run(self):
        print("running run")
        while True:
            print("waiting enter...")
            keyboard.wait(fight.KEY)
            p = threading.Thread(target=fight.fight_voice_play)
            self.speaks.append(p)
            p.start()

    def stop(self):
        self.p.terminate()
        for t in self.speaks:
            t.join()


def greeting(*_):
    return "何だてめえ"


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


def now(*_):
    n = datetime.datetime.now()
    return f"{n.year}年{n.month}月{n.day}日の{n.hour}時{n.minute}分だが何だ?"


def today(*_):
    n = datetime.datetime.today()
    return f"{n.year}年{n.month}月{n.day}日だが何だ?"


def day(*_):
    n = datetime.datetime.today()
    return f"{week[n.weekday()]}だが何だ？"


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


def fight_start(*_):
    global fight_process
    fight_process = Fight()
    return "よっしゃケンカしたる"


def fight_finish(*_):
    if fight_process is None:
        return "いや今ケンカしとらんぞ？"
    fight_process.stop()
    return "ケンカ終わりにするでー"


def finish(*_):
    # print("called finish")
    return Finish


def error():
    return random.choice(["あんだって？", "やべえエラー出た。"])


rq_fun: list[tuple[str, Callable]] = [
    ("オワリニシテ", finish),
    ("ネエシズカニ", greeting),
    ("ココドコ", address),
    ("イマナンジ", now),
    ("キョウナンニチ", today),
    ("キョウナンヨウビ", day),
    ("ケンカカイシ", fight_start),
    ("ケンカオワリ", fight_finish),
    (".+トハ", meaning),
]


def main(rq: str) -> str:
    try:
        req = ""
        for token in tokenizer.tokenize(rq):
            req += token.reading
        req = req.replace("*", "")
        print(req)
        for word, func in rq_fun:
            if re.match(word, req):
                return func(rq, req)
        print("not key")
        return error()
        # return rq_fun[m]()
    except Exception:
        return error()


if __name__ == "__main__":
    print(main("今日は何の日?"))
