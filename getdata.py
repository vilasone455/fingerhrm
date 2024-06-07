# import argparse
from zk import ZK
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

@retry(stop=stop_after_attempt(3) , wait=wait_fixed(2))
def send_attendance(employee_id):
    data = {"employee_id": employee_id}
    api_path = "/api/attendance"
    host = "https://hrm.sokxaygroup.com"
    url = host + api_path
    response = requests.post(url, json=data)

    if response.status_code == 500 or response.status_code == 408:
        raise Exception
    return response.json()
ipName = input("Enter your ip: ") 

# parser = argparse.ArgumentParser(description="Connect to ZK device")
# parser.add_argument('ipName', type=str, help="IP address of the ZK device")

# Parse arguments
# args = parser.parse_args()

# ipName = args.ipName

conn = None
zk = ZK(ipName, port=4370, timeout=10, password=0, force_udp=True, ommit_ping=True)
try:
    conn = zk.connect()

    conn.disable_device()

    conn.read_sizes()

    print("connection success")

    for attendance in conn.live_capture():
        if attendance is None:
            pass
        else:
            employee_id = attendance.user_id
            print("check : " , employee_id)
            try:
                res = send_attendance(employee_id) 
                print(res['message'])
            except Exception as e:
                print("Error occurred:", e)
                print("Retrying...")

    conn.enable_device()
except Exception as e:
    print (format(e))
finally:
    if conn:
        conn.disconnect()