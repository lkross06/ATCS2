import redis
import sqlite3

#Part 1: Key-based Databases
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

r.set("panda", "bamboo")
r.set("eel", "seaweed")
r.set("mako", 12)
r.set(7, "banana")
r.set(10, 4)
r.set("animals", "".join(['panda','lemming','sheep'])) #must be bytes, string, int or float
r.set("user1", "{ name: Sea, age: 3542, birthday: 1/32/-1500 }")

for key in ["panda", "eel", "mako", 7, 10, "animals", "user1"]:
    print(key, r.get(key), sep="\t")

#Part 2: Table-based Databases
conn = sqlite3.connect("users.db")
cur = conn.cursor()

def set_something(query):
    cur.execute(query)
    conn.commit()

def get_something(query):
    cur.execute(query)

    for row in cur.fetchall():
        for col in row:
            print(col, end="\t")
        print()

'''
create table users (id integer primary key, username text, password text, salt text);

insert into users (username, password, salt) values ("bsea", "PANDAS!", "BAMBOO"), ("fern", "Gully", "mooses"), ("brakeman", "mental", "mices"), ("andy", "ateapples", "Battle");

select * from users;

1|bsea|PANDAS!|BAMBOO
2|fern|Gully|mooses
3|brakeman|mental|mices
4|andy|ateapples|Battle
'''

set_something("create table if not exists users (id integer primary key, username text, password text, salt text);")
set_something('insert into users (username, password, salt) values ("bsea", "PANDAS!", "BAMBOO"), ("fern", "Gully", "mooses"), ("brakeman", "mental", "mices"), ("andy", "ateapples", "Battle");')
get_something("select * from users;")

'''
create table if not exists profiles (id integer primary key, user_id integer, color text, hand text, dept text, "group" integer default 5);

insert into profiles (user_id, color, hand, dept, "group") values (2, "red", "right", "math", 20), (1, "green", "right", "math", 22), (4, "purple", "ambi", "english", 12);
insert into profiles (user_id, color, hand, dept) values (3, "red", "left", "science");

select color, dept from profiles;

red|math
green|math
purple|english
red|science

select * from profiles where hand = "right";

1|2|red|right|math|20
2|1|green|right|math|22

select * from users inner join profiles on users.id = profiles.user_id where length(users.password) > 6 and profiles.hand = "right";

1|bsea|PANDAS!|BAMBOO|2|1|green|right|math|22

select users.username from users inner join profiles on users.id = profiles.user_id where users.salt like "B%" and profiles."group" > 10 order by users.username asc;

andy
bsea
'''

set_something('create table if not exists profiles (id integer primary key, user_id integer, color text, hand text, dept text, "group" integer default 5);')
set_something('insert into profiles (user_id, color, hand, dept, "group") values (2, "red", "right", "math", 20), (1, "green", "right", "math", 22), (4, "purple", "ambi", "english", 12);')
set_something('insert into profiles (user_id, color, hand, dept) values (3, "red", "left", "science");')
get_something('select color, dept from profiles;')
get_something('select * from profiles where hand = "right";')
get_something('select * from users inner join profiles on users.id = profiles.user_id where length(users.password) > 6 and profiles.hand = "right";')
get_something('select users.username from users inner join profiles on users.id = profiles.user_id where users.salt like "B%" and profiles."group" > 10 order by users.username asc;')
