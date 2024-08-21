import socket
import threading

from fastapi import FastAPI

from src.app import SocketServer
from src.devices.device_a import DeviceA
from src.devices.device_b import DeviceB
from src.devices.modul_c import ModulC

app = FastAPI()


def send_data(data: str) -> bytes:
    ip = "localhost"
    port = 8000
    data = data.encode()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, port))
        s.sendall(data)
        response = s.recv(1024)
    return response


@app.get("/device/a")
async def get_device_a_status():
    response = send_data("a_status")
    return {"data_a": response}


@app.get("/device/b")
async def get_device_b_status():
    response = send_data("b_status")
    return {"data_b": response}


@app.get("/device/b/increment")
async def device_b_change():
    response = send_data("b_change_increment")
    return {"increment_b": response}


@app.get("/modul/c")
async def get_module_c_status():
    response = send_data("c_status")
    return {"data_c": response}


if __name__ == "__main__":
    lock = threading.Lock()
    server = SocketServer()
    server.start()
    device_a = DeviceA(lock)
    device_b = DeviceB(lock)
    modul_c = ModulC(lock)
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)
