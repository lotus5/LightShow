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
from enum import Enum

class Style(Enum):
    CHANGE = 0
    FADE = 1
    GLOW = 2
    FLASH = 3

def fade(light: str):
    for i in range(100, 10, -5):
        lk.set_brightness(i, light)

def action(light: str, color_tuple, act: Style):
    if act == Style.CHANGE:
        lk.set_color(color_tuple, light)
    else:
        fade(light)
        

# Replace old serials with Tasmota device names
light0_sn = "Light_20"
light1_sn = "Light_71"
light2_sn = "Light_80"

# Turn lights off before starting
lk.power_off(light0_sn)
sleep(0.2)
lk.power_off(light1_sn)
sleep(0.2)
lk.power_off(light2_sn)
sleep(0.7)


# Lightshow timecode array
info_array = [
    # --- INTRO
    
    # Bass drum
    (0.69, light0_sn, (23, 0, 200), Style.CHANGE),
    (1.25, light0_sn, (255, 20, 255), Style.CHANGE),
    
    (2.756, light1_sn, (100, 5, 255), Style.FADE),  # snare
    
    (3.46, light0_sn, (23, 0, 255), Style.FADE),
    (3.47, light0_sn, (23, 200, 255), Style.FADE),
    (4.03, light2_sn, (255, 20, 255), Style.FADE),
    
    # --- guitar
    
]

def start():

    mixer.init()
    mixer.music.load("ZCXsong.mp3")     
    mixer.music.play()
    
    next_act = info_array[0][3]
    next_color = info_array[0][2]
    next_light = info_array[0][1]
    next_time_code = info_array[0][0]
    start_time = time()
    i = 0

    sleep(0.5)

    while i < len(info_array):
        current_time = time() - start_time
        
        if current_time >= next_time_code:
            # lk.set_color(next_color, next_light)
            action(next_light, next_color, next_act)
            print("Time: " + str(next_time_code) + " i: " + str(i))
            next_time_code = info_array[i][0]
            next_light = info_array[i][1]
            next_color = info_array[i][2]
            next_act = info_array[i][3]
            i += 1
            
    sleep(1.2)

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