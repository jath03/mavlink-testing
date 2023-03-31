from pymavlink import mavutil

CONNECTION_STRING = "udpin:0.0.0.0:14550"
DRONE_IDS = [3, 4]


def wait_heartbeats_multi(connection):
    heartbeats = {id: False for id in DRONE_IDS}
    while not all(heartbeats.values()):
        msg = connection.recv_match(type="HEARTBEAT")
        if msg:
            heartbeats[msg.get_srcSystem()] = True


def connect():
    connection = mavutil.mavlink_connection(CONNECTION_STRING)
    connection.wait_heartbeat()
    wait_heartbeats_multi(connection)

    return connection


def recv_ack(connection):
    while True:
        msg = connection.recv_match(type="COMMAND_ACK", blocking=True)
        if msg.get_srcSystem() == connection.target_system:
            break
    print("Received ACK:", msg)


def for_all_drones(f):
    def wrapped(connection, *args, **kwargs):
        for drone in DRONE_IDS:
            connection.target_system = drone
            f(connection, *args, **kwargs)

    return wrapped
