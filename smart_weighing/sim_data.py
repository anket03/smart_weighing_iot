import pymssql
import time
import random

# Connect to SQL Server
try:
    conn = pymssql.connect(server='IN01W-JZM1SV3',
                           user='sa',
                           password='mt',
                           database='iot')
    print('SQL connection successful')
except Exception as e:
    print('SQL connection failed:', e)

# Create a cursor object
cursor = conn.cursor()

def generate_data():
    batch = random.choice(['A', 'B'])
    user = random.choice(['POOJA', 'WICK', 'JOHN', 'JENNY'])
    gross = random.randint(1, 20)
    tare = random.randint(0, 5)
    net = gross - tare
    product = random.choice(['Coffee', 'Tea', 'Bread', 'Flour'])
    # Make sure only one of is_underweight, is_overweight, or is_valid is set to True
    flags = [False, False, False]
    idx = random.randint(0, 2)
    flags[idx] = True
    
    is_underweight = flags[0]
    is_overweight = flags[1]
    is_valid = flags[2]

       
    data = (batch, user, gross, tare, net, product, is_underweight, is_overweight, is_valid)
    return data

# Main loop to send random data on 10 sec interval
while True:
    # Generate random data
    data = generate_data()
    print(data)
    # Insert data into SQL Server
    sql = 'INSERT INTO pi_sql (batch, [user], gross, tare, net, product, is_underweight, is_overweight, is_valid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(sql, data)
    
    # Commit changes
    conn.commit()
    print('Data inserted successfully')
    
    # Wait for 10 seconds
    time.sleep(60)
