import os

import requests


def _api_url(path):
    return "https://api.feedbin.com/v2/" + path


def _credentials():
    return requests.auth.HTTPBasicAuth(
        os.getenv("FEEDBIN_USER"), os.getenv("FEEDBIN_PASSWORD")
    )


def _get(path, params=None):
    return requests.get(_api_url(path), auth=_credentials(), params=params)


def _delete(path, data={}):
    headers = {"content-type": "application/json"}

    return requests.delete(
        _api_url(path), auth=_credentials(), headers=headers, data=data
    )


def check_authenticated():
    return _get("authentication.json").status_code == 200


def get_starred_entries():
    return _get("starred_entries.json").json()


def get_entry_urls(entries):
    entries_list = ",".join([str(id) for id in entries])
    entries_params = {"ids": entries_list}

    response = _get("entries.json", params=entries_params)

    return {entry["id"]: entry["url"] for entry in response.json()}