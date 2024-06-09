import re
from typing import Callable

from janome.tokenizer import Tokenizer

from .address import address
from .error import error
from .fight import fight_finish, fight_start
from .meaning import meaning
from .time import day, now, today

tokenizer = Tokenizer()


class Finish:
    def __init__(self):
        pass


def finish(*_):
    # print("called finish")
    return Finish


def greeting(*_):
    return "何だてめえ"


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
