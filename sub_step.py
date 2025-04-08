import time
import json
import paho.mqtt.client as mqtt

import board
import busio
from adafruit_seesaw.seesaw import Seesaw
from adafruit_crickit import crickit  # This gives you the Crickit object on Pi


# Initialize Seesaw over I2C (required for Crickit HAT to work)
i2c = busio.I2C(board.SCL, board.SDA)
ss = Seesaw(i2c, addr=0x49)  # Default address for Crickit

# Use built-in stepper motor from Crickit HAT
motor = crickit.stepper_motor

# Spin motor forward a few steps
def spin_motor(steps=50, delay=0.01):
    print("Spinning motor...")
    for _ in range(steps):
        motor.onestep()
        time.sleep(delay)
    print("Motor spin done.")

# MQTT callback: runs when client connects
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("pythontest/sensors/mysensor")
    else:
        print(f"Connection failed with code {rc}")

# MQTT callback: runs when message is received
def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Raw message received: {payload}")
    try:
        data = json.loads(payload)  # Parse JSON string
        temp = float(data.get("temperature", -1))
        print(f"Parsed temperature: {temp}")
        if temp > 24:
            spin_motor()
        else:
            print("Temperature below threshold. Not spinning.")
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Invalid message: {e}")

# Set up MQTT subscriber
subscriber = mqtt.Client()
subscriber.on_connect = on_connect
subscriber.on_message = on_message

print("Connecting to broker...")
subscriber.connect("test.mosquitto.org", 1883, 60)
subscriber.loop_start()

# Keep the program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
    subscriber.loop_stop()
    subscriber.disconnect()




