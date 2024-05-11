#THIS FILE IS FOR TEST PURPOSES ONLY. SIMPLY LISTS EVERY CONNECTION FROM P2P.PY
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

clients = r.lrange("connections", 0, -1)
for client in clients:
    print(client)

if len(clients) == 0:
    print("nothing is in connections")