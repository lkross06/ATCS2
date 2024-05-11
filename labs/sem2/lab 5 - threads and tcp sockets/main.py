import getopt
import sys
import redis
import socket
import threading

#literals
__REDIS_PORT = 6379
__REDIS_KEY = "connections"
__SOCKET_PORT = 8082

#global variable
running = True

def listening_socket():
    global running

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(("0.0.0.0", __SOCKET_PORT)) #create server endpoint

    server.listen(10) #10 clients allowed in queue

    while running:
        try:
            conn, (a, i) = server.accept()
            message = conn.recv(1024).decode()
            if message != "":
                print(f"[{a}] {message}")
        except BlockingIOError:
            print("thread blocked")
            continue
    server.close()
    

try:
    __MY_HOSTNAME = socket.gethostname()
    __MY_IP = socket.gethostbyname(__MY_HOSTNAME)
    print(__MY_HOSTNAME, __MY_IP)
except:
    print("Error: cannot resolve hostname")
    quit()

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
removes everything from the redis list under the specified literal key

:param r: redis connection to wipe from

:return: True if successful, False otherwise
'''
def redis_clear(r) -> bool:
    try:
        #remove everything from redis
        while(r.llen(__REDIS_KEY) > 0):
            r.lpop(__REDIS_KEY)
        return True
    except:
        return False

'''
gets command line arguments and executes program
'''
def main():
    global running

    #connect to redis
    r = redis.Redis(host="localhost", port=__REDIS_PORT, decode_responses=True)

    #get num command-line argument
    opts = None
    NUM = None

    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "n:")

        for opt, arg in opts:
            if opt == "-n":
                NUM = int(arg)
                if NUM <= 0:
                    #doesn't really matter, goes to except anyways
                    raise ValueError("num must be positive integer") 
        
        if NUM == None:
            raise ValueError("num not specified")
    except:
        print("Error: invalid number. use \"-n <number>\" flag")
        quit()

    #start a new thread to listen on
    server_thread = threading.Thread(target=listening_socket)
    server_thread.start()

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

            #add to redis
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

    #re-call the server one more time to update and close it
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.connect((__MY_IP, __SOCKET_PORT))
    proxy.close()

    server_thread.join() 

    redis_clear(r) #dont want to fill up my memory

main()