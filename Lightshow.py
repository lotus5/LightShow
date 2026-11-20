# Mi Gente Lightshow using sounddevice instead of PyAudio
# Works on Mac and Windows
# Clap once to start the lightshow

import time
import numpy as np
from array import array
from time import time, sleep

import sounddevice as sd
from pygame import mixer
import LightKitMQTT as lk


def start():
    # Replace old serials with Tasmota device names
    light0_sn = "Light_09"
    light1_sn = "Light_10"
    light2_sn = "Light_29"

    # Turn lights off before starting
    lk.power_off(light0_sn)
    sleep(0.2)
    lk.power_off(light1_sn)
    sleep(0.2)
    lk.power_off(light2_sn)
    sleep(0.7)

    mixer.init()
    mixer.music.load("AMsong.mp3")
    mixer.music.play()

    # Lightshow timecode array
    info_array = [
        (0.9, light0_sn, (23, 0, 255)),
        (1.1, light0_sn, (2, 20, 255)),
        (1.8, light1_sn, (23, 0, 255)),
        (2, light1_sn, (2, 20, 255)),
        (2.8, light2_sn, (23, 0, 255)),
        (3, light2_sn, (2, 20, 255)),
        (4.3, light0_sn, (0, 0, 0)),
        (4.4, light1_sn, (0, 0, 0)),
        (4.5, light2_sn, (0, 0, 0)),

        # after freeze 1
        (5.8, light0_sn, (255, 12, 34)),
        (6.8, light1_sn, (255, 12, 34)),
        (7.9, light2_sn, (255, 12, 34)),
        (8.7, light0_sn, (0, 0, 0)),
        (8.8, light1_sn, (0, 0, 0)),
        (8.9, light2_sn, (0, 0, 0)),

        # after freeze 2
        (10.5, light0_sn, (85, 107, 13)),
        (11.5, light1_sn, (85, 107, 13)),
        (12.5, light2_sn, (85, 107, 13)),
        (13.5, light0_sn, (0, 0, 0)),
        (13.6, light1_sn, (0, 0, 0)),
        (13.7, light2_sn, (0, 0, 0)),

        # after freeze 3
        (14.9, light0_sn, (22, 100, 0)),
        (16, light1_sn, (22, 100, 0)),
        (17.1, light2_sn, (22, 100, 0)),
        (18.2, light0_sn, (0, 0, 0)),
        (18.3, light1_sn, (0, 0, 0)),
        (18.4, light2_sn, (0, 0, 0)),

        # y donde estan mi gente
        (19.4, light0_sn, (255, 128, 0)),
        (19.9, light1_sn, (255, 128, 0)),
        (20.4, light2_sn, (255, 128, 0)),
        (20.9, light0_sn, (0, 0, 0)),
        (20.95, light1_sn, (0, 0, 0)),
        (21, light2_sn, (0, 0, 0)),

        (21.6, light0_sn, (200, 250, 80)),
        (22.1, light1_sn, (200, 250, 80)),
        (22.6, light2_sn, (200, 250, 80)),
        (23.2, light0_sn, (0, 0, 0)),
        (23.3, light1_sn, (0, 0, 0)),
        (23.4, light2_sn, (0, 0, 0)),

        (24, light0_sn, (165, 42, 42)),
        (24.6, light1_sn, (165, 42, 42)),
        (25.2, light2_sn, (165, 42, 42)),
        (25.8, light0_sn, (0, 0, 0)),
        (25.9, light1_sn, (0, 0, 0)),
        (26, light2_sn, (0, 0, 0)),

        # 1 2 3 4
        (26.5, light0_sn, (255, 0, 0)),
        (27.1, light1_sn, (0, 255, 0)),
        (27.7, light2_sn, (0, 0, 255)),
        (28.2, light0_sn, (200, 200, 0)),
        (28.3, light1_sn, (200, 200, 0)),
        (28.4, light2_sn, (200, 200, 0)),

        # crazy part
        (29, light0_sn, (0, 102, 255)),
        (29.6, light1_sn, (103, 0, 255)),
        (30.1, light2_sn, (127, 0, 255)),
        (30.6, light0_sn, (0, 0, 0)),
        (30.7, light1_sn, (0, 0, 0)),
        (30.8, light2_sn, (0, 0, 0)),

        (31.3, light0_sn, (165, 42, 42)),
        (31.9, light1_sn, (165, 42, 42)),
        (32.5, light2_sn, (165, 42, 42)),
        (33.1, light0_sn, (0, 0, 0)),
        (33.2, light1_sn, (0, 0, 0)),
        (33.3, light2_sn, (0, 0, 0)),

        (33.9, light0_sn, (0, 255, 0)),
        (34.5, light1_sn, (0, 128, 255)),
        (35.1, light2_sn, (0, 128, 255)),
        (36.2, light0_sn, (0, 0, 0)),
        (36.3, light1_sn, (0, 0, 0)),
        (36.4, light2_sn, (0, 0, 0))
    ]

    next_color = (0, 255, 255)
    next_light = light0_sn
    next_time_code = 0.0
    start_time = time()
    next_index = 1

    sleep(0.6)

    while next_index < len(info_array):
        current_time = time() - start_time

        if current_time >= next_time_code:
            lk.set_color(next_color, next_light)

            next_change = info_array[next_index]
            next_time_code = next_change[0]
            next_light = next_change[1]
            next_color = next_change[2]
            next_index += 1

    sleep(0.7)

    lk.power_off(light1_sn)
    sleep(0.2)
    lk.power_off(light0_sn)
    sleep(0.2)
    lk.power_off(light2_sn)

    mixer.music.stop()
    global endShow
    endShow = True


# ---------------------------------------------------------
# Clap detection (new: real-time stream, works on Win + Mac)
# ---------------------------------------------------------

endShow = False
CHUNK = 2048
RATE = 44100

# Windows laptops tend to need a higher threshold
threshold = 2000

triggered = False

print("Clap detection initialized")

def audio_callback(indata, frames, t, status):
    global triggered
    if triggered:
        return

    # Peak amplitude of audio chunk
    level = np.max(np.abs(indata))

    if level > threshold:
        print("Clapped")
        triggered = True
        start()


# Continuous listening loop
with sd.InputStream(
    samplerate=RATE,
    channels=1,
    dtype="int16",
    blocksize=CHUNK,
    callback=audio_callback
):
    while not endShow:
        sleep(0.05)