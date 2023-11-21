# cs361_microservice
A logging microservice for a file server
Supports logging and querying
By: Remy Rouyer
[video](https://youtu.be/gkbwhYxPiL4)
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
* Host arg is host IP address to bind the server (default: 127.0.0.1)
* Port arg is the port number to bind the server (default: 9942)
* Mongodb_client arg is the MongoDB client connection string (default: mongodb://localhost:27017/)

## How to request data
![alt text](https://github.com/rouyerr/cs361_microservice/blob/main/uml.png?raw=true)
The client.py shows an example of how to send and recieve log and query requests from the server.
Example Socket connection in python:

            def send_json(socket, msg_dict):
                msg_json = json.dumps(msg_dict)
                msg_bytes = msg_json.encode('utf-8') + b'\x04'
                socket.sendall(msg_bytes)

            def recv_json(server_socket):
                buffer = b""
                while True:
                    data = server_socket.recv(1024)
                    if not data:
                        break
                    buffer += data
                    if b'\x04' in buffer:
                        break
                msg_json = buffer[:-1].decode('utf-8').strip()
                msg_dict = json.loads(msg_json)
                return msg_dict

            def send_recv(host='127.0.0.1', port=9942, request=None):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                    server_socket.connect((host, port))
                    print(recv_json(server_socket))
                    print(f"Request being sent to server: {request}")
                    send_json(server_socket, request)
                    response = recv_json(server_socket)
                    print(f"Server's response: {response}")
                    return response


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
                "query_db": "event_logs",
                "filter": {},
                "limit": int
                start_time": int,
                end_time": int
                }}
Response from logging service from a query will be in the form:

            {"data": [{},{}], #list of matching query json objects
              "recieved": {} # json object of query recieved and fulfiled by server
              }
            }



example Response :

            {"data": [
                {
                  "_id": 2,
                  "file_name": "constitutionV2.txt",
                  "file_type": "txt",
                  "file_size": "10099",
                  "status": "live",
                  "time_created": 1610000000,
                  "last_modified": 1620000000,
                  "downloads": 1,
                  "file_owner": "george",
                  "access_log": [
                    {
                      "_id": "655c52925848071f505ab29a",
                      "file_id": 2,
                      "time": 1650000000,
                      "user": "arnold",
                      "event_type": "download"
                    }
                  ],
                  "update_log": [
                    {
                      "_id": "655c52905848071f505ab296",
                      "file_id": 2,
                      "time": 1620000000,
                      "file_name": "constitutionV2.txt",
                      "file_type": "txt",
                      "file_size": "10099",
                      "user": "george",
                      "event_type": "update"
                    }
                  ]
                }
              ],
              "recieved": {
                "action": "query",
                "data": {
                  "query_db": "file_logs",
                  "filter": { "_id": 2 }
                }
              }
            }
