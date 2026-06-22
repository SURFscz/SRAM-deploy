# 2026-06-22

import requests, json
from datetime import datetime

# Database ID van app waarvan de expiries van de members van de gekoppelde samenwerkingen gewist moeten worden
app_id = 74

user = "<test-user>"
password = "<test-password>"
base_url = "https://test.sram.surf.nl/"
path_get_app = "api/collaborations/by_service_optimized/"
path_get_co = "api/collaborations/"
path_put_expiry = "api/collaboration_memberships/expiry"
headers = {'content-type': 'application/json'}

# Bereik waarbinnen de bestaande expiry moet vallen om gewist te worden
target_date_start = int(datetime(2026, 8, 1, 0, 0).timestamp())
target_date_end = int(datetime(2026, 8, 31, 23, 59).timestamp())

# Aan app gekoppelde samenwerkingen
def get_co_list(app: int) -> list[int]:
    response: str = requests.get(base_url+path_get_app+str(app), auth=(user, password), headers=headers)
    response_list: list = response.json()
    co_list: list = []
    for co in response_list:
        co_list.append(co["id"])
    return co_list

# Leden van samenwerking waarvan bestaande expiry binnen het bereik valt
def get_co_members(co: int) -> list[int]:
    response: str = requests.get(base_url+path_get_co+str(co), auth=(user, password), headers=headers)
    response_dict: dict = response.json()
    memberships: dict = response_dict["collaboration_memberships"]
    member_list: list = []
    for member in memberships:
        if member["expiry_date"] != None and target_date_start <= int(member["expiry_date"]) <= target_date_end:
            member_list.append(member["id"])
    return member_list

# Wis expiry van lidmaatschap
def remove_expiry(co: int, member: int):
    data = { "collaboration_id":co, "membership_id":member, "expiry_date":None }
    response = requests.put(base_url+path_put_expiry, auth=(user, password), headers=headers, json=data)

def main():
    co_list = get_co_list(app_id)
    cos_members: dict = {}
    for co in co_list:
        if get_co_members(co):
            cos_members[co] = get_co_members(co)
    for co in cos_members:
        for member in cos_members[co]:
            remove_expiry(co, member)

main()