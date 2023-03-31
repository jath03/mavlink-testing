from utils import connect, for_all_drones, send_command
from arm import arm, disarm
import time


@for_all_drones
def takeoff(connection, height):
    send_command(connection, 'MAV_CMD_NAV_TAKEOFF_LOCAL', 0, p3=0.3, p7=height)


@for_all_drones
def land(connection):
    send_command(connection, 'MAV_CMD_NAV_LAND_LOCAL', 0, p2=.25, p3=.3, p7=0)


def main():
    connection = connect()

    arm(connection)
    takeoff(connection, 1)
    time.sleep(5)
    land(connection)
    disarm(connection)


if __name__ == "__main__":
    main()
