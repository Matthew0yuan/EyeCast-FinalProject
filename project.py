import csv
import json
import time
import paho.mqtt.client as mqtt
#pip install paho-mqtt
# MQTT broker details
broker_address = 'your-ec2-public-dns'
broker_port = 8883  # Use 1883 for unsecured
username = 'your_username'
password = 'your_password'
topic = 'your/topic'

# MQTT client setup
client = mqtt.Client()
client.username_pw_set(username, password)

# For TLS
client.tls_set(ca_certs='/path/to/mosquitto.crt')
client.tls_insecure_set(True)  # Use only if using self-signed certs

# Connect to broker
client.connect(broker_address, broker_port)

# Read CSV and publish data
csv_file = 'data.csv'
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        message = json.dumps(row)
        client.publish(topic, message)
        print(f'Published: {message} to topic: {topic}')
        time.sleep(1)

# Disconnect
client.disconnect()
