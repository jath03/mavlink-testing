from pymavlink import mavutil
import motioncapture
from utils import connect, send_command, for_all_drones
import time
import datetime


@for_all_drones
def send_vision_data(connection, x, y, z, rx, ry, rz):
    send_command(connection, "VISION_POSITION_ESTIMATE", 0, datetime.datetime.now().microsecond, x, y, z, rx, ry, rz)


def main():
    connection = connect()
    mc = motioncapture.connect("vicon", "192.168.1.1")

    while True:
        mc.waitForNextFrame()
        for name, obj in mc.rigidBodies.items():
            send_vision_data(connection, *obj.position, obj.rotation.x, obj.rotation.y, obj.rotation.z)


if __name__ == "__main__":
    main()
