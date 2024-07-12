from janome.tokenizer import Tokenizer

tokenizer = Tokenizer()


def googlesearch(rq, _):
    words = []
    for word in tokenizer.tokenize(rq):
        if word.part_of_speech.split(",")[0] in ("名詞", "動詞", "形容詞"):
            words.append(word.surface)
    if len(words) == 0:
        raise Exception()
    return (
        f"[{' '.join(words)}]" + f"(https://www.google.com/search?q={'+'.join(words)})"
    )
