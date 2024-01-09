import socket
import threading
import json
import logging

HOST = '127.0.0.1'
PORT = 65432
queues = {}

def handle_client(client_socket, address):
    print(f"Connected by {address}")

    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break

            print(f"Request from {address}: {data}")

            command, *args = data.split()
            response = handle_command(command, args, client_socket)

            client_socket.sendall(response.encode())
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        try:
            remove_client_from_queues(client_socket)
            client_socket.close()
            print(f"Client {address} disconnected")
        except Exception as e:
            print(f"Error closing client socket: {e}")

def handle_command(command, args, client_socket):
    if command == "get_open_queues":
        return json.dumps({"queues": list(queues.keys())})

    elif command == "get_queue_info":
        queue_data = {}

        queue_id = args[0]
        queue = queues.get(queue_id, {"error": "Queue not found"})

        if "error" not in queue:
            queue_data = {
                "users": [{"name": user["name"]} for user in queue["users"]],  # Exclude sockets
                "ready_status": queue["ready_status"],
            }

        return json.dumps(queue_data)

    elif command == "create_queue":
        queue_id = str(len(queues) + 1)
        queues[queue_id] = {"users": [], "ready_status": [], "owner": client_socket}
        return json.dumps({"queue_id": queue_id})

    elif command == "join_queue":
        queue_id = args[0]
        name = args[1]
        queues[queue_id]["users"].append({"name": name, "socket": client_socket})
        queues[queue_id]["ready_status"].append(False)
        return json.dumps({"message": "Joined queue successfully"})

    elif command == "leave_queue":
        queue_id = args[0]
        remove_user_from_queue(queue_id, client_socket)
        if not queues[queue_id]["users"]:
            del queues[queue_id]
        return json.dumps({"message": "Left queue successfully"})

    elif command == "ready":
        queue_id = args[0]
        mark_user_ready(queue_id, client_socket)
        return json.dumps({"message": "Marked as ready"})
        
    else:
        return json.dumps({"error": "Invalid command"})

def remove_user_from_queue(queue_id, client_socket):
    for i, user in enumerate(queues[queue_id]["users"]):
        if user["socket"] == client_socket:
            del queues[queue_id]["users"][i]
            del queues[queue_id]["ready_status"][i]
            break

def mark_user_ready(queue_id, client_socket):
    for i, user in enumerate(queues[queue_id]["users"]):
        if user["socket"] == client_socket:
            queues[queue_id]["ready_status"][i] = True
            break

def remove_client_from_queues(client_socket):
    for queue_id, queue_data in queues.items():
        if queue_data["owner"] == client_socket:
            del queues[queue_id]
            print(f"Queue {queue_id} removed due to owner disconnection")
            break
        else:
            remove_user_from_queue(queue_id, client_socket)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
