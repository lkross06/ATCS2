import threading
import sys
import getopt
import socket
import time
import redis

'''
redis is only needed to let the google drive and the tcp/udp programs communicate

should have four threads in the same file:
- listening tcp (needs a proxy message to stop)
- broadcasting udp
- listening udp (needs a proxy message to stop)
- keyboard/main thread (should loop through threads and .join() them)
'''

#LITERALS
__SOCKET_PORT = 8082
__REDIS_PORT = 6379
__REDIS_KEY = "connections"

#thread-related
threads = []
running = True

#tcp clients
clients = []

#connections / redis
connections_lock = threading.Lock()
connections = {}
r = redis.Redis(host="localhost", port=__REDIS_PORT, decode_responses=True)

try:
    __MY_HOSTNAME = socket.gethostname()
    __MY_IP = socket.gethostbyname(__MY_HOSTNAME)

    #sometimes it just gives the loopback address
    if __MY_IP == "127.0.0.1": 
        #get more info about the IP and retrieve the true ipv4 address
        __MY_IP = socket.gethostbyname_ex(__MY_HOSTNAME)[2][1]
    print(__MY_HOSTNAME, __MY_IP)
except socket.gaierror:
    print("Error: could not resolve hostname")
except Exception as e:
    print(f"Error: {e}")

'''
checks a string to see if its a valid ipv4 address
valid ipv4 addresses should look like "xxx.xxx.xxx.xxx" where x's = digits

:param ip: string ipv4 address to check

:return: True if valid, False otherwise
'''
def check_ipv4_addr(ip) -> bool:
    try:
        arr = str(ip).split(".")

        #check to make sure there's 4 numbers separated by "."
        if len(arr) != 4:
            raise ValueError("invalid ipv4 address")

        #check to make sure all sections are only positive integers
        for n in arr:
            n = int(n)
            if n < 0 or n > 255:
                raise ValueError("invalid ipv4 address")
            
        return True
    except:
        return False

'''
refreshes redis connections every 5 seconds, deletes any connections that have
not sent a message in over 30 seconds
'''
def refresh_redis():
    global running

    while running:
        #initial value of 6, sleep for 5 seconds (6 * 5 = 30)
        #benefit to using 5 seconds is that when running = false it takes at most 5 seconds for the thread to close
        time.sleep(5) 

        print("[RR] refreshing redis...")

        for addr in connections:
            connections[addr] = connections[addr] - 1
            #lock redis access
            connections_lock.acquire()
            if connections.get(addr) == 0: #if it hasnt been refreshed in 30 seconds, remove it
                r.lrem(__REDIS_KEY, count=0, value=addr)
                connections.pop(addr)
            connections_lock.release()

'''
listens for incoming tcp connections and adds to redis database
'''
def listen_tcp():
    global running

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(("0.0.0.0", __SOCKET_PORT)) #create server endpoint

    server.listen(10) #10 clients allowed in queue

    while running:
        try:
            conn, (a, i) = server.accept()
            message = conn.recv(1024).decode()
            if message != "":
                print(f"[L TCP] [{a}] {message}")

                connections_lock.acquire()
                #don't store your own ip, might cause problems later
                if connections.get(a) == None and a != __MY_IP:
                    connections[a] = 6
                    r.lpush(__REDIS_KEY, a)
                else:
                    connections[a] = 6
                connections_lock.release()

        except BlockingIOError:
            print("[L TCP] thread blocked")
            continue
    server.close()

'''
broadcasts udp messages every 5 seconds
'''
def broadcast_udp():
    global running
    
    message = f"Hello, I am {__MY_IP} and my number is {NUM}"
    broadcasting_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broadcasting_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    broadcasting_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcasting_socket.bind(("", __SOCKET_PORT))

    while running:
        time.sleep(5)

        print("[B UDP] broadcasting message...")

        broadcasting_socket.sendto(message.encode(), ("255.255.255.255", __SOCKET_PORT))

    broadcasting_socket.close()

'''
listens for incoming udp connections, adds to redis database
'''
def listen_udp():
    global running

    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    listening_socket.bind(("", __SOCKET_PORT))

    while running:
        try:
            bytes, (recv_address, i) = listening_socket.recvfrom(1024)
            message = bytes.decode()
            if message != "":
                print(f"[L UDP] [{recv_address}] {message}")

                #add to redis IF its not there (lock the connections too!)
                connections_lock.acquire()
                if connections.get(recv_address) == None and recv_address != __MY_IP:
                    connections[recv_address] = 6
                    r.lpush(__REDIS_KEY, recv_address)
                else:
                    connections[recv_address] = 6
                connections_lock.release()

        except BlockingIOError:
            print("thread blocked")
            continue

    listening_socket.close()

#get num command-line argument
opts = None
NUM = None
b_given = False

argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "bn:")

for opt, arg in opts:
    if opt == "-b":
        b_given = True
    if opt == "-n":
        try:
            NUM = int(arg)
            if NUM <= 0:
                raise ValueError() #doesnt really matter
        except:
            quit()

if b_given:
    broadcasting_thread = threading.Thread(target=broadcast_udp)
    broadcasting_thread.start()
    threads.append(broadcasting_thread)

#start two listening threads/sockets
listening_udp_thread = threading.Thread(target=listen_udp)
listening_udp_thread.start()
threads.append(listening_udp_thread)

listening_tcp_thread = threading.Thread(target=listen_tcp)
listening_tcp_thread.start()
threads.append(listening_tcp_thread)

#start the refreshing thread for redis
refreshing_thread = threading.Thread(target=refresh_redis)
refreshing_thread.start()
threads.append(refreshing_thread)

#get other ipv4 address
clients = []

ADDRESS = input("Enter IPv4 Address (0 to quit): ")
while running and ADDRESS != "0":
    if not(check_ipv4_addr(ADDRESS)):
        print("Error: invalid IPv4 address")
        break

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    try:
        client.connect((ADDRESS, __SOCKET_PORT))
        clients.append(client)
        print(f"client connected to {ADDRESS}:{__SOCKET_PORT}")

        #add to redis if its not in there already
        if r.lpos(__REDIS_KEY, ADDRESS) == None:
            r.lpush(__REDIS_KEY, ADDRESS)
        print(f"RECVD: {ADDRESS} {NUM}")

        client.send(f"Hello, I am {__MY_IP} and my number is {NUM}".encode())
    except:
        print(f"Error: could not connect to {ADDRESS}")

    print("-" * 20)
    ADDRESS = input("Enter IPv4 Address (0 to quit): ")

running = False

for client in clients:
    client.close()

#recall the listening sockets for tcp and udp to stop them
tcp_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_proxy.connect((__MY_IP, __SOCKET_PORT))
tcp_proxy.close()

udp_proxy = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
udp_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
udp_proxy.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
udp_proxy.bind(("", __SOCKET_PORT))
udp_proxy.sendto("close please".encode(), (__MY_IP, __SOCKET_PORT))
udp_proxy.close()

#join threads
for thread in threads:
    thread.join()

#clear redis
for key in r.lrange(__REDIS_KEY, 0, -1):
    r.lpop(__REDIS_KEY)