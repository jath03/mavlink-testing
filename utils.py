from pymavlink import mavutil
from contextlib import nullcontext

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


def send_command(connection, cmd, confirm, p1=0, p2=0, p3=0, p4=0, p5=0, p6=0, p7=0, lock=nullcontext(), ack=True):
    if type(cmd) == str:
        try:
            cmd = getattr(mavutil.mavlink, cmd)
        except AttributeError:
            raise AttributeError(f"Unknown command `{cmd}`")
    with lock:
        connection.mav.command_long_send(
            connection.target_system,
            connection.target_component,
            cmd,
            confirm, p1, p2, p3, p4, p5, p6, p7
        )
        if ack:
            recv_ack(connection)
