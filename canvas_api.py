import requests

BASE_URL = "https://gmc.instructure.com"


def suspend_user(sis_user_id, headers):
    url = f"{BASE_URL}/api/v1/users/sis_user_id:{sis_user_id}"
    payload = {"user[event]": "suspend"}
    r = requests.put(url, headers=headers, data=payload)
    r.raise_for_status()


def unsuspend_user(sis_user_id, headers):
    url = f"{BASE_URL}/api/v1/users/sis_user_id:{sis_user_id}"
    payload = {"user[event]": "unsuspend"}
    r = requests.put(url, headers=headers, data=payload)
    r.raise_for_status()
