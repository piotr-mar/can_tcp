import socket
import threading
import time
from typing import Union


class ModulC:
    _device_id: bytes = b"33 44 55 66"
    _frame_type: bytes = b"85"

    def __init__(self, lock):
        self.lock = lock
        self.value_a = None
        self.value_b = None
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(("localhost", 8000))
        self._socket.sendall(b"C")
        self._stop_event = threading.Event()
        self._thread_recv = threading.Thread(target=self.receive_data)
        self._thread_send = threading.Thread(target=self.send_data)
        self._thread_recv.start()
        self._thread_send.start()

    def get_current_data(self, data: int) -> bytes:
        if not data:
            return b"No data from device A and B"
        number_str = str(data)
        number_str = number_str.zfill(10)
        byte_pairs = [number_str[i:i + 2] for i in range(0, len(number_str), 2)]
        result_str = ' '.join(byte_pairs)
        result_bytes = result_str.encode('utf-8')
        result_bytes = self._frame_type + b" " + self._device_id + b" " + result_bytes
        return result_bytes

    def receive_data(self) -> None:
        while True:
            resp = self._socket.recv(1024)
            print(resp)
            data = resp.decode().split(";")
            self.value_a = data[0][16:]
            self.value_b = data[1][16:]
            time.sleep(0.1)

    def sum_values(self) -> Union[int, None]:
        if self.value_b and self.value_a:
            value_a = int(self.value_a.replace(" ", "").lstrip("0"))
            value_b = int(self.value_b.replace(" ", "").lstrip("0"))
            return value_a + value_b
        return None

    def send_data(self) -> None:
        while True:
            data = self.get_current_data(self.sum_values())
            print(data)
            self._socket.sendall(data)
            time.sleep(0.1)

    def stop(self) -> None:
        """Stop the increment thread."""
        self._stop_event.set()
        self._thread_recv.join()
        self._thread_send.join()
