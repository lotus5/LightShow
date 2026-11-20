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
    light0_sn = "Light_54"
    light1_sn = "Light_67"
    light2_sn = "Light_79"

    # Turn lights off before starting
    lk.power_off(light0_sn)
    sleep(0.2)
    lk.power_off(light1_sn)
    sleep(0.2)
    lk.power_off(light2_sn)
    sleep(0.7)

    mixer.init()
    mixer.music.load("ZCXsong.mp3")     # TODO: add wav file
    mixer.music.play()

    # Lightshow timecode array
    info_array = [
        
        # Bass drum
        (0.69, light0_sn, (23, 0, 255)),
        (1.25, light0_sn, (255, 20, 255)),
        
        (2.756, light2_sn, (100, 5, 255)),  # snare
        
        (3.46, light1_sn, (23, 0, 255)),
        (4.03, light1_sn, (255, 20, 255)),
        
        (5.45, light0_sn, (100, 5, 255)),
        
        (5.85, light2_sn, (23, 0, 255)),
        (6.19, light2_sn, (255, 20, 255)),
        (6.69, light0_sn, (2, 20, 255)),
        
        
        
        (8.97, light1_sn, (2, 20, 255)),
        (9.51, light2_sn, (2, 20, 255)),
        
        (11.43, light0_sn, (255, 12, 34)),
        (11.72, light1_sn, (255, 12, 34)),
        (12.2, light2_sn, (255, 12, 34)),
        
        # TODO: WIP, add timestamps for instruments
    ]


    next_color = info_array[0][2]
    next_light = info_array[0][1]
    next_time_code = info_array[0][0]
    start_time = time()
    i = 0

    sleep(0.5)

    # TODO: fix while loop
    while i < len(info_array):
        current_time = time() - start_time

        if current_time >= next_time_code:
            lk.set_color(next_color, next_light)

            next_change = info_array[i]
            next_time_code = next_change[0]
            next_light = next_change[1]
            next_color = next_change[2]
            i += 1
            
    sleep(0.2)

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