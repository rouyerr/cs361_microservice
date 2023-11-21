# cs361_microservice
A logging microservice for a file server
Supports logging and querying
By: Remy Rouyer

# Requirements
install of [mongoDb](https://www.mongodb.com/try/download/community)

# Dependencies
pip install pymongo

## Starting up server
For now supports local mongoDB instances
Run your MongoDB instance. No need to change any configs or inititialize anything.
run LoggingMicroservice.py by calling

            python .\LoggingMicroservice.py [--host host] [--port port] [--mongodb_client]
The args are optional and have defaults:
Host arg is host IP address to bind the server (default: 127.0.0.1)
Port arg is the port number to bind the server (default: 9942)
Mongodb_client arg is the MongoDB client connection string (default: mongodb://localhost:27017/)

## How to request data
![alt text](https://github.com/rouyerr/cs361_microservice/blob/main/uml.png?raw=true)
The client.py shows an example of how to send and recieve log and query requests from the server.
Logging is achieved by sending a json object in the form

            {"action":"log",
            "data":{ "file_id": (unique int),
                    "event_type": "upload"|"download"|"update"}}
                    
You can add any other entries as well, for example.

            {"action":"log",
            "data":{ "file_id": (unique int),
                    "time": int,
                    "file_name": str,
                    "file_type" : str,
                    "file_size": int,
                    "user": str,
                    "event_type": "upload"|"download"|"update"}}
Queries requuests are sent by json objects in the form

      {"action": "query",
        "data": {
                "query_db": "file_logs"|"event_logs",
                "filter": {},
                "limit": int
                }}
Inside the filter dictionary you can insert a key and value you want to match for all the queries.
For example

              {"action": "query",
                "data": {
                    "query_db": "event_logs",
                    "filter": {"user":"unsuspecting_user"}
                }}
or

                {"action": "query",
                "data": {
                    "query_db": "event_logs",
                    "filter": {"event_type":"server_task"}
                }}
or   

                {"action": "query",
                "data": {
                    "query_db": "file_logs",
                    "filter": {"_id":2},
                }}
file_log queries will query the file log objects and the event_logs the event log objects
limit can be omitted or set to 0 to return all matchng queries
for file_log queries you can specifiy none, any or all of the following time entries.

      {"action": "query",
        "data": {
                "query_db": "file_logs",
                "filter": {},
                "limit": int
                "create_start_time": int,
                "create_end_time": int,
                "update_start_time": int,
                "update_end_time": int
                }}
A start_time entry will return everything matching at or after that epoch time for either the files creation or modify time.
A end_time entry is the everything matching on or before that epoch time.
You can specify both for a range.

Likewise for event logs there are start_time and end_time...

      {"action": "query",
        "data": {
                "query_db": "file_logs",
                "filter": {},
                "limit": int
                start_time": int,
                end_time": int
                }}
