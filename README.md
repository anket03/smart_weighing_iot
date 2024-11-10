# Set Up IoT Devices with AWS IoT Core
a.Create an IoT Thing for Each Device:
b.Register Certificates:
c.Define MQTT Topics:

# Step 2: Configure AWS IoT Core for Data Routing
  a."Create IoT Rules":
  b.Testing MQTT Topics:
    Go to Test > MQTT test client and subscribe to your topic (e.g., myiotdevice/telemetry) to monitor incoming data.

# Step 3: Set Up Data Processing with AWS Lambda
  a.Create a Lambda Function:
  b.Write Lambda Code:
  c.Set Up Lambda Trigger : Go to AWS IoT Core, and in Message Routing > Rules, create a new rule.
                            Set the SQL query to capture all messages from your topic, e.g., SELECT * FROM 'myiotdevice/telemetry'.
                            Add an action to invoke your Lambda function, selecting the function you just created.

# Step 4: Set Up DynamoDB for Data Storage                           
  a.Create DynamoDB Table:
  b.Verify Data Ingestion:

# Step 5: Set Up Alerts and Notifications with AWS SNS
  a.Create an SNS Topic:
  b.Set Up Alerts Based on Thresholds:
  
# Step 5: Set Up API Gateway for Data Retrieval  
  Create a New REST API
  Integrate with Lambda:

# Step 6: Set Up Cognito for User Authentication

# streamlit.py - dashboard creation
# pi.py - rasberi pi to aws mqtt data transfer
# sim.py - simulated data store to db 
