import requests


def test_get_open_pull_reqs(app_config):
    base_url = app_config.url["base"]
    repo = app_config.url["ursus_repo"]

    r = requests.get(base_url + repo + "/pulls?state=open")

    assert len(r.json()) == 2
    assert r.json()[0]["url"] == base_url + repo + "/pulls/5"
    assert r.json()[0]["state"] == "open"
    assert r.json()[0]["title"] == "random comment added"


def test_get_closed_pull_reqs(app_config):
    base_url = app_config.url["base"]
    repo = app_config.url["ursus_repo"]

    r = requests.get(base_url + repo + "/pulls?state=closed")

    assert len(r.json()) == 1
    assert r.json()[0]["url"] == base_url + repo + "/pulls/6"
    assert r.json()[0]["state"] == "closed"
    assert r.json()[0]["title"] == "we don't need admin.py"


def test_get_branches_list(app_config):
    base_url = app_config.url["base"]
    repo = app_config.url["ursus_repo"]

    r = requests.get(base_url + repo + "/branches")
    json_data = r.json()
    all_branches = list()
    for el in json_data:
        all_branches.append(el["name"])

    assert len(all_branches) == 30
