from uuid import uuid4
from copy import deepcopy
from schemas import Service
services = dict()
i = 0


def add_user(db, username, service_id):
    global services
    if service_id in services:
        services[service_id]["allowed"].append(username)
        return services[service_id]
    return None


def create_service(db, owner, service, service_name):
    global services
    global i
    entity = {"owner":owner, "allowed":[owner], "service_name":service_name, "service":service, "id":i}
    services[i] = entity
    i += 1
    return entity


def search_all_allowed_services(db, user):
    global services
    out = []
    for j in services:
        if user in services[j]["allowed"]:
            out.append(services[j]["id"])
    return out


def get_service(db, user, id):
    global services
    if id in services:
        if user in services[id]["allowed"]:
            return services[id]
    return None


def delete_service(db, user, id):
    global services
    if id in services:
        if user in services[id]["allowed"]:
            tmp = deepcopy(services[id])
            del services[id]
            return tmp
    return None

