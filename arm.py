from pymavlink import mavutil
from utils import connect, recv_ack
import time

def arm(connection):
    connection.mav.command_long_send(connection.target_system, connection.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)
    recv_ack(connection)    


def disarm(connection):
    connection.mav.command_long_send(connection.target_system, connection.target_component, mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0, 0)    
    recv_ack(connection)

def main():
    connections = connect()
    
    map(arm, connections)
    time.sleep(10)
    map(disarm, connections)
    


if __name__ == "__main__":
    main()