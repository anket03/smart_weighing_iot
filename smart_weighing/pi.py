import socket
import boto3
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import random
import time
from datetime import datetime

# AWS IoT endpoint
iot_endpoint = "a28qrv9tj2231a-ats.iot.ap-south-1.amazonaws.com"

# AWS IoT credentials
iot_client_id = "your-client-id"
iot_root_ca_path = "/home/pi/Desktop/aws_cert/AmazonRootCA1.pem"
iot_private_key_path = "/home/pi/Desktop/aws_cert/private.pem.key"
iot_certificate_path = "/home/pi/Desktop/aws_cert/certificate.pem.crt"

# Initialize AWS IoT MQTT Client
mqtt_client = AWSIoTMQTTClient(iot_client_id)
mqtt_client.configureEndpoint(iot_endpoint, 8883)
mqtt_client.configureCredentials(iot_root_ca_path, iot_private_key_path, iot_certificate_path)

# AWS IoT Core configuration
mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
mqtt_client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
mqtt_client.configureDrainingFrequency(2)  # Draining: 2 Hz
mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

# Connect to AWS IoT
mqtt_client.connect()   
print("Connected to AWS IoT")

# Define the topic
topic = "sql_server"

# Set up TCP/IP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '192.168.0.2'  # Replace with your host name or IP address
port = 1702  # Replace with your port number
s.connect((host, port))

# Receive data in a loop
while True:
    data = s.recv(1024)  # Receive up to 1024 bytes of data
    if not data:
        # If the received data is empty, the socket has been closed
        break
    print("Received data: ", data.decode())
    # Publish the message to AWS IoT
    payload = data.decode()  # Convert bytes to str
    mqtt_client.publish(topic, json.dumps(payload), 1)

# Close the socket
s.close() 
