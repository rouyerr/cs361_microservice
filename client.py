import socket
import json

def send_json(sock, msg_dict):
    msg_json = json.dumps(msg_dict)
    msg_bytes = msg_json.encode('utf-8') + b'\u0004'
    sock.sendall(msg_bytes)

def recv_json(server_socket):
    buffer = b""
    while True:
        data = server_socket.recv(1024)
        if not data:
            break
        buffer += data
        if b'\u0004' in buffer:
            break
    msg_json = buffer[:-6].decode('utf-8').strip()
    msg_dict = json.loads(msg_json)
    return msg_dict

def send_recv(host='127.0.0.1', port=9942, request=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.connect((host, port))
        print(request)
        send_json(server_sock, request)
        response = recv_json(server_sock)
        print(f"Server's response: {response}")
        return response

def populate_with_samples():
    requests = [{"action":"log",
            "data":{ "file_id": 0,
                    "time": 1600000000,
                    "file_name": "never_gonna_let_you_down.txt",
                    "file_type" : "txt",
                    "file_size": "426942",
                    "user": "rick",
                    "event_type": "upload"}},
            {"action":"log",
            "data":{ "file_id": 1,
                    "time": 1600000005,
                    "file_name": "never_gonna_give_you_up.txt",
                    "file_type" : "txt",
                    "file_size": "429942",
                    "user": "rick",
                    "event_type": "upload"}},
            {"action":"log",
                "data":{ "file_id": 0,
                    "time": 1600350500,
                    "user": "unsuspecting_user",
                    "event_type": "download"}},
            {"action":"log",
                "data":{ "file_id": 1,
                    "time": 1600350501,
                    "user": "unsuspecting_user",
                    "event_type": "download"}},
            {"action":"log",
                "data":{ "file_id": 2,
                    "time": 1610000000,
                    "file_name": "constitution.txt",
                    "file_type" : "txt",
                    "file_size": "9999",
                    "user": "george",
                    "event_type": "upload"}},
            {"action":"log",
                "data":{ "file_id": 3,
                    "time": 1615000000,
                    "file_name": "barfuss am klavier.mp3",
                    "file_type" : "mp3",
                    "file_size": "9999",
                    "user": "AnnenMayKantereit",
                    "event_type": "upload"}},
            {"action":"log",
                "data":{ "file_id": 4,
                    "time": 1616000000,
                    "file_name": "toms diner.mp3",
                    "file_type" : "mp3",
                    "file_size": "9999",
                    "user": "AnnenMayKantereit",
                    "event_type": "upload"}},
            {"action":"log",
                "data":{ "file_id": 5,
                    "time": 1617000000,
                    "file_name": "cherry wine.mp3",
                    "file_type" : "mp3",
                    "file_size": "9999",
                    "user": "Hozier",
                    "event_type": "upload"}},
            {"action":"log",
                "data":{ "file_id": 2,
                    "time": 1620000000,
                    "file_name": "constitutionV2.txt",
                    "file_type" : "txt",
                    "file_size": "10099",
                    "user": "george",
                    "event_type": "update"}},
            {"action":"log",
                "data":{ "time": 1630000000,
                    "server_status_code": 418,
                    "message": "I am a teapot",
                    "ip": "192.168.1.1",
                    "event_type": "server_response"}},
            {"action":"log",
                "data":{ "time": 1640000000,
                    "task":"reboot_subservice.exe",
                    "exit_code": 0,
                    "user": "admin",
                    "event_type": "server_task"}},
            {"action":"log",
                "data":{ "time": 1641000000,
                    "task":"reboot_subservice.exe",
                    "exit_code": 0,
                    "user": "admin",
                    "event_type": "server_task"}},
            {"action":"log",
                "data":{ "file_id": 2,
                    "time": 1650000000,
                    "user": "arnold",
                    "event_type": "download"}},
            {"action":"log",
                "data":{ "time": 1651000000,
                    "task":"reboot_subservice.exe",
                    "exit_code": 1,
                    "user": "admin",
                    "event_type": "server_task"}},
            {"action":"log",
                "data":{ "file_id": 3,
                    "time": 1690350300,
                    "user": "remy",
                    "event_type": "download"}},
            {"action":"log",
                "data":{ "file_id": 4,
                    "time": 1690350400,
                    "user": "remy",
                    "event_type": "download"}},
            {"action":"log",
                "data":{ "file_id": 5,
                    "time": 1690350500,
                    "user": "remy",
                    "event_type": "download"}},
            {"action":"log",
                "data":{ "file_id": 0,
                    "time": 1700350500,
                    "user": "unsuspecting_user",
                    "event_type": "download"}},
            {"action":"log",
                "data":{ "file_id": 1,
                    "time": 1700350501,
                    "user": "unsuspecting_user",
                    "event_type": "download"}
            }
                    ]

    for r in requests:
        send_recv(request=r)
        input("enter for next")

def sample_queries():
    queries = [{"action": "query",
                "data": {
                    "query_db": "file_logs",
                    "filter": {},
                }},
               {"action": "query",
                "data": {
                    "query_db": "file_logs",
                    "filter": {},
                    "limit":3
                }},
                {"action": "query",
                "data": {
                    "query_db": "file_logs",
                    "filter": {},
                    "create_start_time": 1615000000
                }},
                {"action": "query",
                "data": {
                    "query_db": "file_logs",
                    "filter": {},
                    "create_start_time": 1615000000,
                    "create_end_time": 1616000000
                }},
                {"action": "query",
                "data": {
                    "query_db": "file_logs",
                    "filter": {},
                    "update_start_time": 1620000000,
                    "update_end_time": 1630000000
                }},
                {"action": "query",
                "data": {
                    "query_db": "file_logs",
                    "filter": {"_id":2},
                }},
                {"action": "query",
                "data": {
                    "query_db": "event_logs",
                    "filter": {},
                }},
                {"action": "query",
                "data": {
                    "query_db": "event_logs",
                    "filter": {},
                    "limit":3
                }},
                {"action": "query",
                "data": {
                    "query_db": "event_logs",
                    "filter": {},
                    "start_time":1690350300
                }},
                {"action": "query",
                "data": {
                    "query_db": "event_logs",
                    "filter": {},
                    "start_time":1600000005,
                    "end_time":1690350000
                }},
                {"action": "query",
                "data": {
                    "query_db": "event_logs",
                    "filter": {"user":"unsuspecting_user"}
                }},
                {"action": "query",
                "data": {
                    "query_db": "event_logs",
                    "filter": {"event_type":"server_task"}
                }},
               ]
    for i,q in enumerate(queries):
        with open(f"query{i}.json","w") as f:
            json.dump(send_recv(request=q),f)
        input("enter for next")

if __name__ == "__main__":
    #populate_with_samples()
    sample_queries()