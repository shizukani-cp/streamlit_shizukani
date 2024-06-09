import datetime

week = ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"]


def now(*_):
    n = datetime.datetime.now()
    return f"{n.year}年{n.month}月{n.day}日の{n.hour}時{n.minute}分だが何だ?"


def today(*_):
    n = datetime.datetime.today()
    return f"{n.year}年{n.month}月{n.day}日だが何だ?"


def day(*_):
    n = datetime.datetime.today()
    return f"{week[n.weekday()]}だが何だ？"
