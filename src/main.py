"""Da Kommentar."""
import select
import socket

ports_receive = {
    "S3": [1616, 0],
    "S4": [1617, 0],
    "B6": [1605, 0],
    "B7": [1606, 0],
    "B8": [1607, 0],
    "B9": [1608, 0],
}

ports_send = {
    "Q4": [1703, 0],
    "Q5": [1704, 0],
    "P1": [1713, 0],
    "E6": [1714, 0],
}

sockets_receive_list = []

socket_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def get_key(val: int) -> str:
    """Da Kommentar."""

    return next(
        (key for key, value in ports_receive.items() if val == value[0]),
        "key doesn't exist",
    )


for dict_data in ports_receive.items():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, dict_data[1][0])
    server_socket.setblocking(False)
    server_socket.bind(("localhost", dict_data[1][0]))
    sockets_receive_list.append(server_socket)


while True:
    try:
        readable, writable, exceptional = select.select(sockets_receive_list, [], [])
        for s in readable:
            try:
                (client_data, client_address) = s.recvfrom(1024)
                print(get_key(client_address[1]), "is", str(client_data, "utf-8"))
                ports_receive[get_key(client_address[1])][1] = int(
                    str(client_data, "utf-8")
                )
            except OSError as e:
                print(f"Error creating socket: {e}")
    except (OSError, ValueError) as e:
        print(f"Error select socket: {e}")

    # da Logik schriebe
    ports_send["Q4"][1] = ports_receive["S3"][1]
    # loop für sendto mache
    socket_send.sendto(
        str.encode(str(ports_send["Q4"][1])), ("localhost", ports_send["Q4"][0])
    )

server_socket.close()
print("Socket closed")
