import boto3
import json
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import pymssql
import random
import time
from datetime import datetime


# AWS IoT credentials
client_id  = "abc-123"
root_ca_path  = r"C:\Users\karadkar-1\Desktop\python\streamlit dashboard\project_1\project_1\aws_cert\AmazonRootCA1.pem"
private_key_path  = r"C:\Users\karadkar-1\Desktop\python\streamlit dashboard\project_1\project_1\aws_cert\private.pem.key"
certificate_path  = r"C:\Users\karadkar-1\Desktop\python\streamlit dashboard\project_1\project_1\aws_cert\certificate.pem.crt"
host  = "a28qrv9tj2231a-ats.iot.ap-south-1.amazonaws.com"
# Subscription parameters
topic = "sql_server"


# SQL server settings
sql_server = "IN01W-JZM1SV3"  # Update with the correct server name
sql_user = "sa"
sql_password = "mt"
sql_database = "iot"
# Connect to SQL Server
try:
    conn = pymssql.connect(sql_server, sql_user, sql_password, sql_database)
    cursor = conn.cursor()
except Exception as e:
    print("Error connecting to SQL Server:", e)
    exit()


# AWS IoT MQTT client setup
myAWSIoTMQTTClient = AWSIoTMQTTClient(client_id)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(root_ca_path, private_key_path, certificate_path)

# AWS IoT MQTT client connection
print("Connecting to AWS IoT...")
myAWSIoTMQTTClient.connect()
print("Connected to AWS IoT!")

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    # Send acknowledgment message if needed
    # ack_message = "Acknowledgment message"
    # myAWSIoTMQTTClient.publish("ack_topic", ack_message, 1)

    try:
        payload = message.payload.decode('utf-8').strip().strip('"').split(',')
        batch = payload[0]
        user = payload[1]
        gross = float(payload[2].replace(' GR', ''))
        tare = float(payload[3].replace(' T', ''))
        net = float(payload[4].replace(' N', ''))
        product = payload[5]
        is_underweight = payload[6]
        is_overweight = payload[7]
        is_valid = payload[8].strip().replace('\\r\\n', '')

        # Insert data into SQL Server
        try:
            cursor.execute("INSERT INTO pi_sql (batch, [user], gross, tare, net, product, is_underweight, is_overweight, is_valid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (batch, user, gross, tare, net, product, is_underweight, is_overweight, is_valid))

            conn.commit()
            print("Data inserted into SQL Server successfully!")
        except Exception as e:
            print("Error inserting data into SQL Server:", e)

    except Exception as e:
        print("Error processing message:", e)

    finally:
        if cursor is None or cursor.rowcount == 0:
            print("No data stored in SQL Server.")
        else:
            print("Data stored in SQL Server.")

# Subscribe to the topic
print("Subscribing to topic:", topic)
myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)
print("Subscribed to topic:", topic)

# Loop to continuously listen for incoming messages
while True:
    pass