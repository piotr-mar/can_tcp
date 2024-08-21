import socket
import threading
import time

import select


class SocketServer:
    def __init__(self, host: str = 'localhost', port: int = 8000):
        self.device_a_value = b'85 22 33 44 55 00 00 00 07 29'
        self.device_b_value = b'85 22 33 44 55 00 00 00 07 29'
        self.modul_c_value = None
        self.device_map = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)
        self.sockets_list = [self.server_socket]
        self.lock = threading.Lock()

    def start(self) -> None:
        threading.Thread(target=self._socket_server).start()

    @staticmethod
    def _restart_watchdog(client_socket: socket) -> None:
        while True:
            try:
                client_socket.send(b"0xFF")
            except Exception as e:
                print(f"Reset watchdog msg send error: {str(e)}")
            time.sleep(0.5)

    def _send_msg_to_modul_c(self, client_socket: socket) -> None:
        while True:
            try:
                msg = self.device_a_value + b";" + self.device_b_value
                client_socket.send(msg)
            except Exception as e:
                print(f"{str(e)}")
            time.sleep(0.1)

    def _handle_message(self, message: bytes, client_socket: socket) -> None:
        print(f"Received message: {message}")
        if message == b"A":
            self.device_map["A"] = client_socket
        elif message == b"B":
            self.device_map["B"] = client_socket
            if not hasattr(self, '_watchdog_thread') or not self._watchdog_thread.is_alive():
                self._watchdog_thread = threading.Thread(target=self._restart_watchdog, args=(client_socket,))
                self._watchdog_thread.start()
        elif message == b"C":
            self._modul_c = threading.Thread(target=self._send_msg_to_modul_c, args=(client_socket,))
            self._modul_c.start()
        else:
            if b"11 22 33 44" in message:
                self.device_a_value = message
            elif b"22 33 44 55" in message:
                self.device_b_value = message
            elif b"33 44 55 66" in message:
                self.modul_c_value = message
            elif message == b"a_status":
                client_socket.send(self.device_a_value)
            elif message == b"b_status":
                client_socket.send(self.device_b_value)
            elif message == b"b_change_increment":
                self._change_increment(client_socket)
            elif message == b"c_status":
                client_socket.send(self.modul_c_value)

    def _change_increment(self, client_socket: socket) -> None:
        device_b_socket = self.device_map.get("B")
        if device_b_socket:
            device_b_socket.send(b"b_increment")
            response = device_b_socket.recv(1024)
            client_socket.send(response)

    def _socket_server(self) -> None:
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

    def _remove_socket(self, client_socket: socket) -> None:
        if client_socket in self.sockets_list:
            self.sockets_list.remove(client_socket)
        client_socket.close()


if __name__ == "__main__":
    server = SocketServer()
    server.start()
