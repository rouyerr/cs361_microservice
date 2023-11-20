
import socket
import threading
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

def log_event(db, event_data_org):

    event_data = event_data_org.copy()
    event_logs = db["event_logs"]
    file_logs = db["file_logs"]
    event_id = event_logs.insert_one(event_data).inserted_id
    if event_data.get("event_type","") == "upload":
        event_data.pop("event_type")
        event_data["status"] = "live"
        event_data["time_created"] = event_data.pop("time")
        event_data["last_modified"] = event_data.get("last_modified",None) or event_data.get("time_created",0)
        event_data["downloads"] = 0
        event_data["file_owner"] = event_data.pop("user")
        event_data["access_log"] = []
        event_data["update_log"] = []
        event_data["_id"] = event_data.pop("file_id")
        file_logs.insert_one(event_data)

    if event_data.get("event_type","") == "download":
        query = {"_id":event_data.get("file_id"), "status": "live"}
        update = {"$inc": {"downloads": 1},
                  "$push": {"access_log": event_id}}
        file = [f for f in file_logs.find(query)]
        if len(file) == 1:
            file_logs.update_one({"_id":file[0].get("_id")}, update)

    if event_data.get("event_type","") == "update":
        event_data.pop("event_type")
        event_data.pop("_id")
        query = {"_id":event_data.pop("file_id"), "status": "live"}
        file = [f for f in file_logs.find(query)]
        event_data["last_modified"] = event_data.pop("time")
        event_data.pop("user")
        
        update = {"$set": {k:v for k,v in event_data.items()},
                  "$push": {"update_log": event_id}}
        print(update)
        
        if len(file) == 1:
            file_logs.update_one({"_id":file[0].get("_id")}, update)

def handle_query(db, query_org):
    response = {}
    query = query_org.copy()
    query_db = query.pop("query_db")
    filters =  query.pop("filter",{})
    limit = query.pop("limit", 0)
    if query_db == "event_logs":
        logs = db[query_db]
        if query.get("start_time",""):
            filters["time"] = {"$gte": query.get("start_time")}
        if query.get("end_time",""):
            filters.get("time",{}).update({"$lte": query.get("end_time")})

        query_response = list(logs.find(filters).limit(limit))
        for qr in query_response:
            qr = serialize_dict(qr)
        response["data"] = list(query_response)
    elif query_db == "file_logs":
        logs = db[query_db]
        if query.get("create_start_time",""):
            filters["time_created"] = {"$gte": query.get("create_start_time")}
        if query.get("create_end_time",""):
            filters.get("time_created",{}).update({"$lte": query.get("create_end_time")})
        if query.get("update_start_time",""):
            filters["last_modified"] = {"$gte": query.get("update_start_time")}
        if query.get("update_end_time",""):
            filters.get("last_modified",{}).update({"$lte": query.get("update_end_time")})

        query_response = list(logs.find(filters).limit(limit))
        event_logs = db["event_logs"]
        for doc in query_response:
            doc["access_log"] = [serialize_dict(event_logs.find_one({"_id": event_id})) for event_id in doc["access_log"]]
            doc["update_log"] = [serialize_dict(event_logs.find_one({"_id": event_id})) for event_id in doc["update_log"]]
        response["data"] = query_response
    else:
        response["error"] = f"{query_db=} not found please use \"file_logs\" or \"event_logs\""
    return response

def serialize_dict(d):
    for k, v in d.items():
        if isinstance(v, ObjectId):
            d[k] = str(v)
        elif isinstance(v, dict):
            d[k] = serialize_dict(v)
    return d

def recv_json(client_socket):
    buffer = b""
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        buffer += data
        if b'\u0004' in buffer:
            break
    msg_json = buffer[:-6].decode('utf-8').strip()
    msg_dict = json.loads(msg_json)
    return msg_dict

def send_json(sock, msg_dict):
    msg_dict = serialize_dict(msg_dict)
    msg_json = json.dumps(msg_dict)
    msg_bytes = msg_json.encode('utf-8') + b'\u0004'
    sock.sendall(msg_bytes)

def handle_client(client_socket, address, db):
    print(f"Connected to {address}")
    
    request = recv_json(client_socket)
    if not request:
        response = {"code":400,
                        "message":f"Received absolutely nodda, nothing,zip"}
    try:
        print(request)
        request_action = request.get("action","")
        response={"recieved": request.copy()}
        if request_action == "log":
            log_event(db, request.get("data"))
            response.update({"code":200,
                        "message":f"Received the request, logging data and closing connection"})
        if request_action == "query":
            response.update(handle_query(db, request.get("data")))
            
        send_json(client_socket, response)
    except json.JSONDecodeError:
        print("Invalid data received")

    client_socket.close()
    print(f"Connection closed for {address}")

def start_server(host='127.0.0.1', port=9942):
    clientdb = MongoClient("mongodb://localhost:27017/")
    db = clientdb["file_server_db"]
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"Listening on {host}:{port}")

    while True:
        client, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client, address,db))
        thread.start()

if __name__ == "__main__":
    start_server()