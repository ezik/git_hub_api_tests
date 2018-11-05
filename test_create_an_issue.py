import requests
from requests.auth import HTTPBasicAuth


def test_create_new_issue(app_config):
    base_url = app_config.url["base"]
    repo = app_config.url["ursus_repo"]
    username = app_config.auth["username"]
    password = app_config.auth["password"]

    r = requests.post(base_url + repo + "/issues",
                      json={
                          "title": "Issue title for test",
                          "body": "Smth doesn't work!",
                          "labels": ["test", "amazing", "new_issue"],
                          "assignees": ["django_test"]
                      }, auth=HTTPBasicAuth(username=username, password=password))

    assert r.json()["repository_url"] == base_url + repo
    assert r.json()["title"] == "Issue title for test"
    assert r.json()["body"] == "Smth doesn't work!"
