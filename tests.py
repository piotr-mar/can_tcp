# # Oryginalny ciąg bajtów
# original_bytes = b'\x12\x34\x56\x78'
#
# modified_bytes = bytearray(13)
# modified_bytes[0] = 0x05
# modified_bytes[1:1+len(original_bytes)] = original_bytes
# formatted_bytes = ''.join(f'\\x{byte:02x}' for byte in bytes(modified_bytes))
# # formatted_bytes = f'b\'{formatted_bytes}\''
# formatted_bytes = formatted_bytes.encode()
# print(formatted_bytes)
#
# # Oryginalna liczba
# original_number = 0x12345678
#
# # Konwersja liczby na 4-bajtowy ciąg w porządku big-endian
# original_bytes = original_number.to_bytes(4, byteorder='big')
#
# # Formatuj każdy bajt do postaci \xNN i połącz wszystko w jeden ciąg
# formatted_bytes = ''.join(f'\\x{byte:02x}' for byte in original_bytes)
#
# # Przekształć to z powrotem do zmiennej typu bytes
# final_bytes = formatted_bytes.encode()
#
# print(final_bytes)


# import asyncio
# import threading
#
#
# class DeviceA:
#     _device_id: hex = 0x11223344
#     _status: int = 1
#     _data: int = 0
#
#     def __init__(self, lock):
#         self.lock = lock
#         self._status = 1
#         self._data = 0
#         self._loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(self._loop)
#         self._task = self._loop.create_task(self.increment())
#         self._loop_thread = threading.Thread(target=self.start_event_loop)
#         self._loop_thread.start()
#
#     def get_device_id(self):
#         return hex(self._device_id)
#
#     async def increment(self):
#         while self._status:
#             await asyncio.sleep(1)
#             if self._data > 999:
#                 self._data = 0
#             else:
#                 self._data += 1
#
#     def get_current_data(self):
#         return self._data
#
#     def start_event_loop(self):
#         """Start the event loop in a non-blocking way."""
#         try:
#             self._loop.run_forever()
#         except KeyboardInterrupt:
#             self._loop.stop()
#         finally:
#             self._loop.close()
#
#     def stop_event_loop(self):
#         """Stop the event loop."""
#         self._status = 0
#         self._loop.call_soon_threadsafe(self._loop.stop)
#         self._loop_thread.join()
#
#
# # Usage
# if __name__ == "__main__":
#     import time
#
#     lock = threading.Lock()  # Example lock, modify as needed
#     device = DeviceA(lock)
#
#     # Allow some time for the device to operate
#     try:
#         for _ in range(10):
#             print(f"Current data: {device.get_current_data()}")
#             time.sleep(1)
#     finally:
#         # Ensure the event loop is stopped and thread is joined
#         device.stop_event_loop()

import threading
import time

# class DeviceA:
#     _device_id: hex = 0x11223344
#     _status: int = 1
#     _data: int = 0
#
#     def __init__(self, lock):
#         self.lock = lock
#         self._status = 1
#         self._data = 0
#         self._stop_event = threading.Event()
#         self._thread = threading.Thread(target=self.increment)
#         self._thread.start()
#
#     def get_device_id(self):
#         return hex(self._device_id)
#
#     def increment(self):
#         while not self._stop_event.is_set():
#             with self.lock:
#                 if self._data > 999:
#                     self._data = 0
#                 else:
#                     self._data += 1
#             time.sleep(0.1)
#
#     def get_current_data(self):
#         with self.lock:
#             return self._data
#
#     def stop(self):
#         """Stop the increment thread."""
#         self._stop_event.set()
#         self._thread.join()
#
# # Usage
# if __name__ == "__main__":
#     lock = threading.Lock()  # Example lock, modify as needed
#     device = DeviceA(lock)
#
#     # Simulate accessing data and waiting
#     try:
#         for _ in range(10):
#             print(f"Current data: {device.get_current_data()}")
#             time.sleep(2)
#     finally:
#         # Stop the increment thread
#         device.stop()

# import socket
#
# def send_command_to_gateway(ip, port, data):
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.connect((ip, port))
#         s.sendall(data)
#         response = s.recv(1024)
#     return response


# Funkcja konwertująca liczbę na odpowiedni format bajtów
# def number_to_byte_format(number):
#     # Konwersja liczby na ciąg znaków
#     number_str = str(number)
#
#     # Dodanie zer na początku, aby ciąg miał zawsze 10 znaków (5 par po 2 cyfry)
#     number_str = number_str.zfill(10)
#
#     # Podział ciągu na pary cyfr
#     byte_pairs = [number_str[i:i + 2] for i in range(0, len(number_str), 2)]
#
#     # Łączenie par z separatorami
#     result_str = ' '.join(byte_pairs)
#
#     # Konwersja na bajty
#     result_bytes = result_str.encode('utf-8')
#
#     return result_bytes
#
#
# # Przykłady użycia
# print(number_to_byte_format(12345678))  # Wyjście: b'00 12 34 56 78'
# print(number_to_byte_format(1234))  # Wyjście: b'00 00 00 12 34'
# print(number_to_byte_format(123))  # Wyjście: b'00 00 00 01 23'

# import select
# import socket
#
# server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.bind(('localhost', 8000))
#
# server_socket.listen(4)
# sockets_list = [server_socket]
#
# print("Serwer nasłuchuje na porcie 8000...")
#
# def handle_client_message(client_socket):
#     try:
#         message = client_socket.recv(1024)
#         if message:
#             print(f"Otrzymano dane: {message}")
#         else:
#             # Połączenie zostało zamknięte
#             sockets_list.remove(client_socket)
#             client_socket.close()
#     except:
#         sockets_list.remove(client_socket)
#         client_socket.close()
#
# while True:
#     read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
#
#     for notified_socket in read_sockets:
#         if notified_socket == server_socket:
#             client_socket, client_address = server_socket.accept()
#             sockets_list.append(client_socket)
#             print(f"Nowe połączenie od {client_address}")
#         else:
#             handle_client_message(notified_socket)
#     for notified_socket in exception_sockets:
#         sockets_list.remove(notified_socket)
#         notified_socket.close()

import socket
import threading
import time
import select


class SocketServer:
    def __init__(self, host='localhost', port=8000):
        self.device_a = None
        self.device_b = None
        self.device_map = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.sockets_list = [self.server_socket]
        self.lock = threading.Lock()

    def start(self):
        threading.Thread(target=self._socket_server).start()

    @staticmethod
    def _restart_watchdog(client_socket):
        while True:
            try:
                client_socket.send(b"0xFF")
            except Exception as e:
                print(f"Reset watchdog msg send error: {str(e)}")
            time.sleep(0.5)

    def _handle_message(self, message, client_socket):
        if message == b"A":
            self.device_map["A"] = client_socket
        elif message == b"B":
            self.device_map["B"] = client_socket
            if not hasattr(self, '_watchdog_thread') or not self._watchdog_thread.is_alive():
                self._watchdog_thread = threading.Thread(target=self._restart_watchdog, args=(client_socket,))
                self._watchdog_thread.start()
        else:
            if b"11 22 33 44" in message:
                self.device_a = message
            elif b"22 33 44 55" in message:
                self.device_b = message
            elif message == b"a_status":
                client_socket.send(self.device_a)
            elif message == b"b_status":
                client_socket.send(self.device_b)
            elif message == b"b_change_increment":
                self._change_increment(client_socket)

    def _change_increment(self, client_socket):
        device_b_socket = self.device_map.get("B")
        if device_b_socket:
            device_b_socket.send(b"b_increment")
            response = device_b_socket.recv(1024)
            client_socket.send(response)

    def _socket_server(self):
        while True:
            read_sockets, _, exception_sockets = select.select(self.sockets_list, [], self.sockets_list)
            for notified_socket in read_sockets:
                if notified_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    self.sockets_list.append(client_socket)
                    print(f"Nowe połączenie od {client_address}")
                else:
                    try:
                        message = notified_socket.recv(1024)
                        if message:
                            self._handle_message(message, notified_socket)
                        else:
                            self._remove_socket(notified_socket)
                    except:
                        self._remove_socket(notified_socket)

            for notified_socket in exception_sockets:
                self._remove_socket(notified_socket)

    def _remove_socket(self, client_socket):
        if client_socket in self.sockets_list:
            self.sockets_list.remove(client_socket)
        client_socket.close()


if __name__ == "__main__":
    server = SocketServer()
    server.start()
