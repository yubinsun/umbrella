# Echo server program
import select
import socket
import threading
import time


class receiver(threading.Thread):
    def __init__(self, host = "", port=50007):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.server_socket = None
        self.active_client = []  # size should be limited to 1
        # todo: maybe set time out for client after inactivity
        self.active = False;
        # self.start = self.run
        self.server_socket_created = False
        self.socket_cleaned = False

    def init_server_socket(self):
        # TODO: consider adding support for other network topology
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(0)  # given we only need to accept one connection
        # TODO: buffer size here
        self.server_socket_created = True

    def get_client_message(self, client: int = 0):
        # TODO what if inactive/ not exist
        try:
            msg = self.active_client[client].recv(4096)
            if msg:
                return msg
                # print(msg)
            else:
                return b''

        except Exception as e:
            pass

    def del_server_socket(self):
        self.server_socket.close()
        print("socket closed")

    def del_client_socket(self):
        for client in self.active_client:
            client.close()

    def __del__(self):
        if not self.socket_cleaned:
            self.del_client_socket()
            self.del_server_socket()
            self.socket_cleaned = True

    def stop(self):
        self.active = False;

    def run(self) -> None:
        if not self.server_socket_created:
            self.init_server_socket()
            self.server_socket_created = True
        self.active = True
        self.server_socket.settimeout(0)
        try:
            while self.active:
                try:
                    time.sleep(0.00001)
                    (conn, addr) = self.server_socket.accept()
                    conn.settimeout(0)
                except BlockingIOError as e:
                    continue
                except socket.timeout as e:
                    continue
                self.active_client.append(conn)
                print("Connection from ", conn, addr)
        except Exception as e:
            print(type(e), e)
        finally:
            self.__del__()


def test_comm():
    r = receiver('', 50007)
    r.init_server_socket()
    r.start()
    try:
        while True:
            time.sleep(0.01)
            (r.get_client_message())
            # print(len(r.active_client))
    except Exception as e:
        print(e)
    finally:
        r.stop()


if __name__ == '__main__':
    test_comm()
