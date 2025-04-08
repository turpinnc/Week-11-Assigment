1. List of Materials (in Markdown format)

No other materials are needed at this time.

2. Circuit Documentation (for Posture Corrector)
Setup: A Raspberry Pi connected to a camera module.
The camera is used to monitor posture. No other components are required for this version.




3. Stepper Motor Control via MQTT (Crickit HAT + Raspberry Pi)
This script runs on a Raspberry Pi with an Adafruit Crickit HAT and spins a stepper motor when a temperature value received over MQTT exceeds 24°C.

Hardware
Raspberry Pi

Adafruit Crickit HAT

Stepper motor (connected to the STEPPER terminals on the Crickit)

5V power supply for the Crickit

Software Setup
Install the required libraries by running:

pip install paho-mqtt adafruit-circuitpython-crickit adafruit-circuitpython-seesaw

Make sure I2C is enabled on the Raspberry Pi. You can do this by running sudo raspi-config, going to Interfaces, and enabling I2C.

Usage
Save the script as step_sub.py, then run it with:

python3 step_sub.py

The script subscribes to the MQTT topic:
pythontest/sensors/mysensor

It listens for JSON-formatted messages, like:

{
  "temperature": 25.4,
  "humidity": 50.2,
  "timestamp": "2025-04-08T13:36:12.808797"
}
Messaging Logic → Motor Control
When a message is received, the script parses the JSON payload.

It extracts the temperature field.

If the temperature is greater than 24°C, the Crickit’s built-in stepper_motor object spins the motor forward a set number of steps.

No action is taken if the temperature is 24°C or below.

This allows the motor to respond in real time to temperature data sent from another device.
```
