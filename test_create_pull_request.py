import requests
from requests.auth import HTTPBasicAuth
import random
import re


def test_create_pull_req(app_config):
    """This test is intended to create pull request. As precondition user has to:
    - Prepare branch basing on existing branches in repo
    - Prepare commit in new branch
    - Create pull request for the commit
    I used own repo on github to ensure that I have rights for pull requests
    Hope comments will add more transparency on what is happening inside
    Assertions in between are used to ensure that all data is created"""
    base_url = app_config.url["base"]
    repo = app_config.url["ezik_repo"]
    username = app_config.auth["username"]
    password = app_config.auth["password"]

    print("\n=====START PRECONDITION STEPS=====")

    get_branches_list_response = requests.get(base_url + repo + "/git/refs/heads")
    branches_list_data = get_branches_list_response.json()
    assert get_branches_list_response.status_code == 200

    sha_list = list()
    for sha in branches_list_data:
        sha_list.append(tuple((sha["ref"], sha["object"]["sha"])))
    assert sha_list[0][0] == "refs/heads/branch_requests_test"

    ref_branch = "{0}_{1}".format(sha_list[0][0], random.choice(range(101, 10000)))  # generate ref branch
    head_branch_name = re.sub(r"refs/heads/", "", ref_branch, flags=re.I)  # substring branch name from ref branch
    print("HEAD BRANCH NAME...\n", head_branch_name)

    create_branch_response = requests.post(base_url + repo + "/git/refs",
                                         json={
                                             "ref": ref_branch,
                                             "sha": sha_list[0][1]
                                         }, auth=HTTPBasicAuth(username=username, password=password))
    assert create_branch_response.status_code == 201

    new_branch_data = create_branch_response.json()
    sha_latest_commit = new_branch_data["object"]["sha"]
    print("LATEST SHA COMMIT...\n", sha_latest_commit)

    sha_base_tree_response = requests.get(base_url + repo + "/git/commits/{}".format(sha_latest_commit))
    assert sha_base_tree_response.status_code == 200

    sha_base_tree_json = sha_base_tree_response.json()
    sha_base_tree = sha_base_tree_json["tree"]["sha"]
    commit_parent = sha_base_tree_json["parents"][0]["sha"]

    create_commit_response = requests.post(base_url + repo + "/git/commits",
                                    json={
                                        "message": "freaking commit",
                                        "tree": sha_base_tree,
                                        "parents": [commit_parent]
                                    }, auth=HTTPBasicAuth(username=username, password=password))
    create_commit_data = create_commit_response.json()
    assert create_commit_data["author"]["name"] == "ezik"
    assert create_commit_data["message"] == "freaking commit"

    print("=====END PRECONDITION STEPS=====")

    create_pull_req_response = requests.post(base_url + repo + "/pulls",
                      json={
                          "title": "Amazing new feature",
                          "body": "Please pull this in!",
                          "head": head_branch_name,
                          "base": "master"
                      }, auth=HTTPBasicAuth(username=username, password=password))

    pull_req_data = create_pull_req_response.json()

    assert create_pull_req_response.status_code == 201
    assert pull_req_data["state"] == "open"
    assert pull_req_data["body"] == "Please pull this in!"
    assert pull_req_data["head"]["ref"] == head_branch_name
