from pymavlink import mavutil
from utils import connect, recv_ack, for_all_drones
import time


@for_all_drones
def arm(connection, force: bool = False):
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 1, 21196 if force else 0, 0, 0, 0, 0, 0
    )
    recv_ack(connection)
    print("Armed drone", connection.target_system)


@for_all_drones
def disarm(connection, force: bool = False):
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
        0, 0, 21196 if force else 0, 0, 0, 0, 0, 0
    )
    recv_ack(connection)
    print("Disarmed drone", connection.target_system)


def main():
    connection = connect()

    arm(connection)
    time.sleep(10)
    disarm(connection)


if __name__ == "__main__":
    main()
