import socket
import threading
import argparse
import pyautogui 
import subprocess

# Setup argument parser
parser = argparse.ArgumentParser(description='Server start-up options')
parser.add_argument("--ip", default='0.0.0.0', type=str, help="IP address the socket server will run on")
parser.add_argument("--port", default=50050, type=int, help="Port the socket server will listen to")

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024) 
            if not data:
                break
            command = data.decode('utf-8').strip()
            print(f"Received: {command}")
            execute_command(command)
    finally:
        client_socket.close()
        print("Connection closed.")

def execute_command(command):
    """Executes a given keyboard command using pyautogui."""
    try:
        if command.lower() in ["up", "down", "left", "right", "enter", "space", "backspace"]:
            cmd = command.lower()
            pyautogui.press(cmd)  # Arrow keys
        else:
            pyautogui.typewrite(command)  # Type the received string
    except Exception as e:
        print(f"Error executing command '{command}': {e}")


# def execute_command(command):
#     """Executes a given keyboard command using xdotool."""
#     key_mappings = {
#         "up": "Up",
#         "down": "Down",
#         "left": "Left",
#         "right": "Right",
#         "enter": "Return",
#         "space": "space"
#     }
    
#     try:
#         command = command.lower()
#         if command in key_mappings:
#             subprocess.run(['xdotool', 'key', key_mappings[command]], check=True)
#         elif len(command) == 1 and command.isalpha():
#             subprocess.run(['xdotool', 'key', command], check=True)
#         else:
#             print(f"Invalid command attempted: {command}")
#     except Exception as e:
#         print(f"Error executing command '{command}': {e}")

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")
    print(f"Type this IP and port into the application to connect. \n IP: {host}\n PORT: {port} \n")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Connected by {addr}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    finally:
        server_socket.close()

if __name__ == '__main__':
    args = parser.parse_args()
    start_server(host=args.ip, port=args.port)
