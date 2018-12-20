# Beats By David - Code

## About Us
Beats By David set out to solve a problem that all college students face, find a quiet, peaceful place to study. Students spend a ton of time search for places that have space, and are a comfortable environment. In our experience, we'll spend around 15 minutes walking all around campus in search for a place to study. By eliminating this arduous process of find someplace to study, we can increase the amount of time students spend studying and help them use their time more effectively.

To accomplish this task, we have developed a service that reports current and historic Sound and Temperature data from remote locations to users. Universities and departments can purchase or make these devices and place them around campus in areas that students are most likely to study. Students can then access a web page that displays this data, and will inform them about which place has the optimal conditions.

In our Beta phase, we made one hardware unit and took it around to different places in the CU Boulder Engineering Center. Students were able to go to http://beats.davidkopala.com/ to view the data that was being published. During our in class demonstration, we had the audience make a lot of noise, and there as a significant increase in the sound level that was displayed to the user.

## Software

The backend of the project is built using a stack of PostgreSQL, Flask, Celery, SQL Alchemy, and Socket IO. The frontend began as a simple HTML page, but was adapted to React to provide easier integration with the middle layer and database.

### Database

The PostgreSQL database has three main tables: Data, Locations, and Devices. The following code will drop and re-create all the tables in the database. Every data point that gets recorded on a device will be stored in the Data table, and will include a Foreign Key that tells us which Device it came, and which Location it came from.

### Server & API

The code runs on an Amazon Web Services (AWS) EC2 server, and is available at publicly at http://beats.davidkopala.com/. A service has been added to systemd that runs the Flask API script, and nginx delivers the static web content for the React app.

#### API

The API is available publicly at http://beats.davidkopala.com:8000/api and follows the JSON-RPC 2.0 protocol. Requests can be sent using a GET request and passing the JSON object as a GET 'r' variable, http://beats.davidkopala.com:8000/api?r={}, or as a POST request with the JSON object in the body data. A sample request and response has been included below, and a larger collection of examples is available in our Postman collection at https://www.getpostman.com/collections/20d7872f9ac63d7b49cb.

Request:
```
{
	"id": "Postman Testing",
	"method": "down.query_data",
	"params": {
		"limit":2,
		"order_by":"id",
		"direction":"DESC"
	}
}
```

Response:
```
{
    "id": "Postman Testing",
    "error": {},
    "result": {
        "raw": [
            {
                "timestamp": 1544108668463.192,
                "value": "67.29688",
                "device": "{\"status\": \"INVALID\", \"decibel\": \"0.0\", \"locationid\": \"1\", \"id\": 1, \"temp\": \"0.0\"}",
                "locationid": 1,
                "deviceid": 1,
                "units": "F",
                "type": "Temperature",
                "id": 6506,
                "location": "{\"latitude\": \"0.000000\", \"id\": 1, \"longitude\": \"0.000000\", \"name\": \"TEST LOCATION\"}"
            }
        ]
    },
    "pass": true
}
```

### Local Development Setup

The application will continue running on the AWS server as long as I keep paying for it, so if you're just looking to see if it works try just using the endpoints discussed above first. However, it is entirely possible to run it locally as well, you'll just need to change the database connection string in config.py in /MiddleLayer to point to a different server if you want. The app is also available as a Docker image. It can be compiled locally using the Dockerfile in MiddleLayer/Dockerfile, or through Docker Hub, at davidkopala/beatsbydavid:submission.

These instruction detail how to run the API on a local machine.

1. Install Python
2. Install Python Dependencies
```
pip install Flask
pip install Celery
pip install SQLAlchemy
pip install flask-socketio
pip install psycopg2
pip install gevent
 ```
3. Install PostgresSQL
```
sudo apt-get install postgresql
```
4. Create A Database and Tables
```
CREATE DATABASE beatsbydavid;

DROP TABLE IF EXISTS data ;
DROP TABLE IF EXISTS devices ; 
DROP TABLE IF EXISTS locations ;

CREATE TABLE devices (
    ID SERIAL PRIMARY KEY,
    Location VARCHAR(50) NOT NULL,
    Status VARCHAR(20) NOT NULL,
    Temp DOUBLE PRECISION NOT NULL,
    Decibel DOUBLE PRECISION NOT NULL
);

CREATE TABLE locations(
    ID SERIAL PRIMARY KEY,
    Name VARCHAR(50) NOT NULL,
    Latitude Decimal(9,6),
    Longitude Decimal(9,6)
);

CREATE TABLE data (
    ID SERIAL PRIMARY KEY,
    LocationID INT REFERENCES locations(ID) NOT NULL,
    DeviceID INT REFERENCES devices(ID) NOT NULL,
    Timestamp TIMESTAMP DEFAULT NOW(),
    Type Varchar(20) NOT NULL,
    Value Decimal(10, 5) NOT NULL,
    Units Varchar (10)
);
```

5. Update config.py
  - Change DB_STRING in MiddleLayer/config.py to point to the new database you just created.
```
postgresql://username:password@ip-address:port/database
```

6. Run the app
```
python APIServer.py
```

## Hardware

- Raspberry Pi Zero W
- Sparkfun Sound Detector
- MCP3002 (2 Channel ADC)
- TMP36 (Temperature Sensor)

### "Firmware"

A python script starts on boot and starts reading data from the ADC every 5 seconds. This data is then packaged into a JSON-RPC request, and is sent to the server.
