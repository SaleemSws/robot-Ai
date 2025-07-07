import time
import csv
from robomaster import robot

if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    ep_chassis = ep_robot.chassis

    # สร้าง log แยกสำหรับแต่ละเซนเซอร์
    logs_position = []
    logs_attitude = []
    logs_imu = []
    logs_esc = []
    logs_status = []
    start_time = time.time()

    def handler_position(info):
        now = round(time.time() - start_time, 2)
        # info: (x, y, z)
        logs_position.append({
            "timestamp": now,
            "x": info[0],
            "y": info[1],
            "z": info[2]
        })
    def handler_attitude(info):
        now = round(time.time() - start_time, 2)
        # info: (yaw, pitch, roll)
        logs_attitude.append({
            "timestamp": now,
            "yaw": info[0],
            "pitch": info[1],
            "roll": info[2]
        })
    def handler_imu(info):
        now = round(time.time() - start_time, 2)
        # info: (acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z)
        logs_imu.append({
            "timestamp": now,
            "acc_x": info[0],
            "acc_y": info[1],
            "acc_z": info[2],
            "gyro_x": info[3],
            "gyro_y": info[4],
            "gyro_z": info[5]
        })
    def handler_esc(info):
        now = round(time.time() - start_time, 2)
        # info: (speed, angle, timestamp, state)
        logs_esc.append({
            "timestamp": now,
            "speed": info[0],
            "angle": info[1],
            "esc_timestamp": info[2],
            "state": info[3]
        })
    def handler_status(info):
        now = round(time.time() - start_time, 2)
        # info: (static_flag, up_hill, down_hill, on_slope, pick_up, slip_flag, impact_x, impact_y, impact_z, roll_over, hill_static)
        logs_status.append({
            "timestamp": now,
            "static_flag": info[0],
            "up_hill": info[1],
            "down_hill": info[2],
            "on_slope": info[3],
            "pick_up": info[4],
            "slip_flag": info[5],
            "impact_x": info[6],
            "impact_y": info[7],
            "impact_z": info[8],
            "roll_over": info[9],
            "hill_static": info[10]
        })

    ep_chassis.sub_position(freq=10, callback=handler_position)
    ep_chassis.sub_attitude(freq=10, callback=handler_attitude)
    ep_chassis.sub_imu(freq=10, callback=handler_imu)
    ep_chassis.sub_esc(freq=10, callback=handler_esc)
    ep_chassis.sub_status(freq=10, callback=handler_status)

    # ขนาด 1 แผ่น = 0.6m, 2 แผ่น = 1.2m
    side = 0.7  # เมตร
    xy_speed = 0.7
    z_speed = 45
    z_val = -90

    for i in range(4):
        ep_chassis.move(x=side, y=0, z=0, xy_speed=xy_speed).wait_for_completed()
        time.sleep(0.5)
        ep_chassis.move(x=0, y=0, z=z_val, z_speed=z_speed).wait_for_completed()
        time.sleep(0.5)

    ep_chassis.unsub_status()
    ep_chassis.unsub_esc()
    ep_chassis.unsub_imu()
    ep_chassis.unsub_attitude()
    ep_chassis.unsub_position()
    ep_robot.close()

    # บันทึก log แยกไฟล์ต่อเซนเซอร์
    with open("position_log.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "x", "y", "z"])
        writer.writeheader()
        writer.writerows(logs_position)
    with open("attitude_log.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "yaw", "pitch", "roll"])
        writer.writeheader()
        writer.writerows(logs_attitude)
    with open("imu_log.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "acc_x", "acc_y", "acc_z", "gyro_x", "gyro_y", "gyro_z"])
        writer.writeheader()
        writer.writerows(logs_imu)
    with open("esc_log.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "speed", "angle", "esc_timestamp", "state"])
        writer.writeheader()
        writer.writerows(logs_esc)
    with open("status_log.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "static_flag", "up_hill", "down_hill", "on_slope", "pick_up", "slip_flag", "impact_x", "impact_y", "impact_z", "roll_over", "hill_static"])
        writer.writeheader()
        writer.writerows(logs_status)
