import redis

client=redis.Redis(
    host='localhost',
    port=6379,
    db=0
)

try:
    response = client.ping()
    print(f"TCP connection is ready,{response}")
except redis.ConnectionError as e:
    print(f"E:{e}")

client.set('name','Aboba')
name = client.get('name')
print(name.decode())
client.delete('name')

if client.exists('name'):
    print("key name is  in db")
else:
    print("Db has no key name")

client.set('users_online',238)
client.incr('users_online')
users_online = client.get('users_online')
print(users_online.decode())