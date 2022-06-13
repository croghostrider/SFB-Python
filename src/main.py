"""Da Kommentar."""
import select
import socket
import time

end_time = time.time() + 0.5
motor_is_moving = False
next_up = True
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

print("Program started")

for dict_data in ports_receive.items():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, dict_data[1][0])
    server_socket.setblocking(False)
    server_socket.bind(("localhost", dict_data[1][0]))
    sockets_receive_list.append(server_socket)


def logik() -> None:
    """Da Kommentar."""
    global motor_is_moving
    global next_up
    if motor_is_moving:
        if ports_receive["B7"][1] == 0:
            ports_send["Q4"][1] = 0
            next_up = False
            motor_is_moving = False
            print("garage door is open")
        elif ports_receive["B8"][1] == 0:
            ports_send["Q5"][1] = 0
            next_up = True
            motor_is_moving = False
            print("garage door is closed")

    if ports_receive["S3"][1] == 1 or ports_receive["S4"][1] == 1:
        if motor_is_moving:
            if ports_send["Q5"][1] == 1:
                ports_send["Q5"][1] = 0
                motor_is_moving = False
                next_up = True
                print("stop garage door, next will it open")
            elif ports_send["Q4"][1] == 1:
                ports_send["Q4"][1] = 0
                motor_is_moving = False
                next_up = False
                print("stop garage door, next will it close")
        elif ports_receive["B7"][1] == 0 or next_up is False:
            ports_send["Q5"][1] = 1
            motor_is_moving = True
            next_up = False
            print("close garage door")
        elif ports_receive["B8"][1] == 0 or next_up is True:
            ports_send["Q4"][1] = 1
            motor_is_moving = True
            next_up = True
            print("open garage door")


def get_key(val: int) -> str:
    """Da Kommentar."""

    return next(
        (key for key, value in ports_receive.items() if val == value[0]),
        "key doesn't exist",
    )


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

    if time.time() > end_time:
        logik()
        end_time = time.time() + 0.5

    # loop für sendto mache
    socket_send.sendto(
        str.encode(str(ports_send["Q4"][1])), ("localhost", ports_send["Q4"][0])
    )

    socket_send.sendto(
        str.encode(str(ports_send["Q5"][1])), ("localhost", ports_send["Q5"][0])
    )

    socket_send.sendto(
        str.encode(str(ports_send["P1"][1])), ("localhost", ports_send["P1"][0])
    )

server_socket.close()
print("Socket closed")
