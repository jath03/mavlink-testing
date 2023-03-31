from pymavlink import mavutil
import time

master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')

master.wait_heartbeat()

while True:
    try:
        msg = master.recv_match(type="HEARTBEAT")
        print(f"[{msg.get_srcSystem()}]", msg.to_dict())
    except Exception:
        pass
    time.sleep(0.1)