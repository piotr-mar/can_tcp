import socket
import threading
import time


class DeviceA:
    _device_id: bytes = b"11 22 33 44"
    _frame_type: bytes = b"85"
    _status: int = 1
    _data: int = 0

    def __init__(self, lock):
        self.lock = lock
        self._status = 1
        self._data = 0
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect(("localhost", 8000))
        self._socket.sendall(b"A")
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self.increment)
        self._thread_send = threading.Thread(target=self.send_data)
        self._thread.start()
        self._thread_send.start()

    def increment(self) -> None:
        while not self._stop_event.is_set():
            with self.lock:
                if self._data > 999:
                    self._data = 0
                else:
                    self._data += 1
            time.sleep(0.1)

    def get_current_data(self) -> bytes:
        with self.lock:
            number_str = str(self._data)
            number_str = number_str.zfill(10)
            byte_pairs = [number_str[i:i + 2] for i in range(0, len(number_str), 2)]
            result_str = ' '.join(byte_pairs)
            result_bytes = result_str.encode('utf-8')
            result_bytes = self._frame_type + b" " + self._device_id + b" " + result_bytes
            return result_bytes

    def send_data(self) -> None:
        while True:
            print(self.get_current_data())
            self._socket.sendall(self.get_current_data())
            time.sleep(0.9)

    def stop(self) -> None:
        """Stop the increment thread."""
        self._stop_event.set()
        self._thread.join()
        self._thread_send.join()
