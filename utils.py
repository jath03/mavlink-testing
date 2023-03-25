from pymavlink import mavutil

CONNECTION_STRING = "udpin:0.0.0.0:14550"
NUM_DRONES = 2


def connect(n: int = NUM_DRONES) -> list["connection"]:
    connections = []
    
    for _ in range(n):
        connection = mavutil.mavlink_connection(CONNECTION_STRING)
        connection.wait_heartbeat()
        print(f"Heartbeat from system (system {connection.target_system} component {connection.target_component})")
        connections.append(connection)
    
    return conections

def recv_ack(connection):
    msg = connection.recv_match(type='COMMAND_ACK', blocking=True)
    print(msg)