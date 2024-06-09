import multiprocessing
import threading

import keyboard
import playsound

KEY = "enter"


fight_process = None


def fight_voice_play():
    playsound.playsound("fight_voice.mp3")


class Fight:
    def __init__(self):
        self.speaks = []
        self.p = multiprocessing.Process(target=self.run)
        self.p.start()

    def run(self):
        print("running run")
        while True:
            print("waiting enter...")
            keyboard.wait(KEY)
            p = threading.Thread(target=fight_voice_play)
            self.speaks.append(p)
            p.start()

    def stop(self):
        self.p.terminate()
        for t in self.speaks:
            t.join()


def fight_start(*_):
    global fight_process
    fight_process = Fight()
    return "よっしゃケンカしたる"


def fight_finish(*_):
    if fight_process is None:
        return "いや今ケンカしとらんぞ？"
    fight_process.stop()
    return "ケンカ終わりにするでー"
