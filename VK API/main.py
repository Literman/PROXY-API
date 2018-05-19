import socket
import requests
import json
import time
from collections import Counter

# https://api.vk.com/method/users.get?
# user_ids=literrman
# &fields=bdate
# &access_token=cee19771de51c0546e15306f0d3184f44bbccd77df4459e534489f70bcbe7db81a9d7001b42f2a28ce0ff
# &v=5.74

API = "https://api.vk.com/method/"
TOKEN = "cee19771de51c0546e15306f0d3184f44bbccd77df4459e534489f70bcbe7db81a9d7001b42f2a28ce0ff"

ID = "95961008"
ID_Tanya = "257824293"


def decode(funk):
    def wrapper(arg1, arg2):
        return json.loads(funk(arg1, arg2).content.decode())['response']
    return wrapper


@decode
def get(method, params):
    return requests.get(f"{API}{method}?{params}&access_token={TOKEN}&v=5.74", timeout=3)


def get_user(nick):
    return get("users.get", f"user_ids={nick}")[0]["id"]


def get_groups(id):
    return get("groups.get", f"user_id={id}")["items"]


def get_friends(id, count):
    return get("friends.get", f"user_id={id}&count={count}")["items"]


def get_groups_info(ids):
    return get("groups.getById", f"group_ids={ids}")


def main():
    groups = Counter()
    my_friends = get_friends(ID, 10)
    for friend in my_friends:
        try: groups += Counter(get_groups(friend))
        except: continue

    time.sleep(1)
    top = groups.most_common(10)
    ids = ','.join((str(place[0]) for place in top))
    for group in get_groups_info(ids):
        print(group['name'])


if __name__ == '__main__':
    main()
