#!/usr/bin/env python3
import requests
import time
import random
import uuid # For a unique worker ID if needed locally, though server assigns primary ID

# --- Configuration ---
MASTER_URL = 'http://localhost:8000/api' # Base API URL of the master server
NODE_IP = f'192.168.1.{random.randint(10, 200)}' # Simulate a dynamic/random IP for testing
# Locations based on Brazilian states for the map
LOCATIONS = ['SP', 'RJ', 'MG', 'BA', 'PR', 'RS', 'SC', 'PE', 'CE', 'AM']
NODE_LOCATION = random.choice(LOCATIONS)
NODE_ID_FROM_SERVER = None # To store the ID received from the master after registration

REGISTER_ENDPOINT = f'{MASTER_URL}/register/'
STATUS_ENDPOINT = f'{MASTER_URL}/status/'
TASK_ENDPOINT = f'{MASTER_URL}/task/'

STATUS_UPDATE_INTERVAL = 30  # seconds
TASK_REQUEST_INTERVAL = 60   # seconds
INITIAL_RETRY_INTERVAL = 5   # seconds for registration attempts

def generate_node_identifier():
    # Could be MAC address, a persistent generated UUID, etc.
    # For this simulation, IP is used as the primary identifier for status updates as per view.
    return NODE_IP

NODE_IDENTIFIER = generate_node_identifier()

def register_node():
    global NODE_ID_FROM_SERVER
    payload = {
        'ip': NODE_IP,
        'location': NODE_LOCATION
    }
    print(f'[{NODE_IDENTIFIER}] Attempting to register with master: {payload}')
    try:
        response = requests.post(REGISTER_ENDPOINT, json=payload)
        response.raise_for_status()  # Raises an exception for 4XX/5XX errors
        registered_node_data = response.json()
        NODE_ID_FROM_SERVER = registered_node_data.get('id')
        print(f'[{NODE_IDENTIFIER}] Successfully registered with master. Node data: {registered_node_data}')
        return True
    except requests.exceptions.RequestException as e:
        print(f'[{NODE_IDENTIFIER}] Failed to register: {e}')
        return False

def send_status_update():
    if not NODE_ID_FROM_SERVER and not NODE_IP: # Must have some identifier
        print(f'[{NODE_IDENTIFIER}] Cannot send status update, node not identified.')
        return

    payload = {
        'ip': NODE_IP, # Using IP to identify the node as per NodeStatusUpdateAPIView
        'status': 'online',
        # 'node_id': NODE_ID_FROM_SERVER, # Could use this if API supports it
        # 'task_result': {} # Placeholder for future task results
    }
    print(f'[{NODE_IDENTIFIER}] Sending status update: {payload}')
    try:
        response = requests.post(STATUS_ENDPOINT, json=payload)
        response.raise_for_status()
        print(f'[{NODE_IDENTIFIER}] Status update successful: {response.json()}')
    except requests.exceptions.RequestException as e:
        print(f'[{NODE_IDENTIFIER}] Failed to send status update: {e}')

def request_task():
    print(f'[{NODE_IDENTIFIER}] Requesting new task...')
    try:
        response = requests.get(TASK_ENDPOINT)
        response.raise_for_status()
        task_data = response.json()
        print(f'[{NODE_IDENTIFIER}] Received task: {task_data}')
        process_task(task_data)
    except requests.exceptions.RequestException as e:
        print(f'[{NODE_IDENTIFIER}] Failed to request task: {e}')
    except ValueError: # Includes JSONDecodeError
        print(f'[{NODE_IDENTIFIER}] Failed to decode task JSON response.')


def process_task(task_data):
    task_type = task_data.get('type')
    if task_type == 'simple_math':
        instruction = task_data.get('instruction')
        data = task_data.get('data', {})
        a = data.get('a')
        b = data.get('b')
        if instruction == 'Add the numbers.' and a is not None and b is not None:
            result = a + b
            print(f'[{NODE_IDENTIFIER}] Task result ({instruction}): {a} + {b} = {result}')
            # Here you could send the result back, e.g., via a status update
        else:
            print(f'[{NODE_IDENTIFIER}] Could not process math task: missing data or unknown instruction.')
    else:
        print(f'[{NODE_IDENTIFIER}] Unknown task type: {task_type}')


if __name__ == '__main__':
    print(f'--- Node Worker ---')
    print(f'Node Identifier (IP for now): {NODE_IDENTIFIER}')
    print(f'Node Location: {NODE_LOCATION}')
    print(f'Master URL: {MASTER_URL}')
    print(f'--------------------')

    # Initial registration attempt loop
    while not register_node():
        print(f'[{NODE_IDENTIFIER}] Retrying registration in {INITIAL_RETRY_INTERVAL} seconds...')
        time.sleep(INITIAL_RETRY_INTERVAL)

    # Main loop for status updates and task requests
    last_status_update = 0
    last_task_request = 0

    try:
        while True:
            current_time = time.time()

            if current_time - last_status_update >= STATUS_UPDATE_INTERVAL:
                send_status_update()
                last_status_update = current_time

            if current_time - last_task_request >= TASK_REQUEST_INTERVAL:
                request_task()
                last_task_request = current_time

            # Sleep for a short interval to prevent busy-waiting
            # Adjust the sleep time based on the smallest interval (status or task)
            time.sleep(min(STATUS_UPDATE_INTERVAL, TASK_REQUEST_INTERVAL) / 5)

    except KeyboardInterrupt:
        print(f'[{NODE_IDENTIFIER}] Worker shutting down.')
    finally:
        # Optionally, send an 'offline' status update on shutdown
        if NODE_IP: # Check if IP was set (registration might have failed)
            print(f'[{NODE_IDENTIFIER}] Sending final offline status...')
            payload = {'ip': NODE_IP, 'status': 'offline'}
            try:
                requests.post(STATUS_ENDPOINT, json=payload, timeout=5) # Short timeout
                print(f'[{NODE_IDENTIFIER}] Offline status sent.')
            except requests.exceptions.RequestException as e:
                print(f'[{NODE_IDENTIFIER}] Failed to send offline status: {e}')
