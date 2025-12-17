import socket
import time
import base64

# --- Configuration ---
HOST = 'localhost'
PORT = 4190
USERNAME = 'test'
PASSWORD = '12345'
# The command used for authentication (SASL PLAIN)
AUTH_STRING = f'\0{USERNAME}\0{PASSWORD}'
SASL_PLAIN_AUTH = base64.b64encode(AUTH_STRING.encode()).decode()

def trigger_broken_pipe():
    print(f"Connecting to {HOST}:{PORT}...")
    try:
        # 1. Establish the connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        print("Connected.")

        # Read the initial banner from the server
        banner = s.recv(1024).decode()
        print(f"Server Banner: {banner.strip()}")

        # 2. Authenticate using SASL PLAIN
        auth_command = f'AUTHENTICATE "PLAIN" "{SASL_PLAIN_AUTH}"\r\n'
        s.sendall(auth_command.encode())
        print("Sent AUTHENTICATE command.")

        # Read the server's authentication response (OK)
        auth_response = s.recv(1024).decode()
        print(f"Auth Response: {auth_response.strip()}")

        # 3. Send the LOGOUT command
        logout_command = 'LOGOUT\r\n'
        s.sendall(logout_command.encode())
        print(f"\nSent: {logout_command.strip()}")

        # --- CRITICAL STEP TO CAUSE THE ERROR ---
        # Instead of waiting for the server's LOGOUT OK response,
        # we immediately close the client's socket.
        print("**Immediately closing client socket to trigger BrokenPipeError on server...**")
        s.close()

    except ConnectionRefusedError:
        print(f"Error: Connection refused. Is pysieved running on {PORT}?")
    except Exception as e:
        print(f"Client encountered an error: {e}")

if __name__ == "__main__":
    trigger_broken_pipe()