# cs361_microservice
A logging microservice for a file server
By: Remy Rouyer

#Requirements
install of mongoDb running locally on the machine

#Dependencies
pip install pymongo


The client.py shows an example of how to send and recieve from the server.
Supports logging and querying
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
