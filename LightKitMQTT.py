"""
LightKitMQTT.py
Helper library for controlling Tasmota light bulbs via MQTT.

This version uses blocking one shot publishes so it behaves
consistently on Mac and Windows.
"""

from time import sleep
import paho.mqtt.publish as publish

# MQTT broker configuration
BROKER = "192.168.0.98"   # change if your Mosquitto IP is different
PORT = 1883


def _publish(topic: str, payload: str):
    """Blocking publish of a single MQTT message."""
    publish.single(
        topic,
        payload,
        hostname=BROKER,
        port=PORT,
        retain=False,
    )


# basic light commands

def power_on(light: str):
    """Turn a light on."""
    topic = f"cmnd/{light}/POWER"
    _publish(topic, "ON")


def power_off(light: str):
    """Turn a light off."""
    topic = f"cmnd/{light}/POWER"
    _publish(topic, "OFF")


def set_color(color_tuple, light: str):
    """
    Set a light RGB color using a 3 tuple (R, G, B).
    Example: set_color((255, 0, 0), "Light_01")
    """
    r, g, b = color_tuple
    payload = f"{r},{g},{b}"
    topic = f"cmnd/{light}/Color"
    _publish(topic, payload)


def set_brightness(level: int, light: str):
    """Set brightness from 0 to 100."""
    topic = f"cmnd/{light}/Dimmer"
    _publish(topic, str(level))


def set_temperature(kelvin: int, light: str):
    """Set white color temperature (Tasmota uses 153 to 500)."""
    topic = f"cmnd/{light}/CT"
    _publish(topic, str(kelvin))


# effect helpers

def flash(light: str, times: int = 1, speed: float = 0.3):
    """Flash the light on and off a number of times."""
    for _ in range(times):
        power_on(light)
        sleep(speed)
        power_off(light)
        sleep(speed)


def pulse_color(color_tuple, light: str, repeats: int = 3, speed: float = 0.5):
    """Pulse a color a few times."""
    for _ in range(repeats):
        set_color(color_tuple, light)
        sleep(speed)
        power_off(light)
        sleep(speed)


def color_cycle(color_list, light: str, delay: float = 1.0):
    """Cycle through a list of RGB tuples."""
    for c in color_list:
        set_color(c, light)
        sleep(delay)


# advanced

def send_cmd(light: str, command: str, payload):
    """
    Send any raw Tasmota command.
    Example: send_cmd("Light_01", "POWER", "ON")
    """
    topic = f"cmnd/{light}/{command}"
    _publish(topic, str(payload))