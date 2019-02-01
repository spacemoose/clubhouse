import sys
from github import Github
import os
import json
import pprint

# I couldn't get token authentification to work, hence this hack:
gh_user = os.environ["GITHUB_USER"]
gh_pass = os.environ["GITHUB_PASSWORD"]
#gh_token = os.environ["GITHUB_TOKEN"]

# path to a JSON file containing mappings from github users to
# clubhouse user ids.
user_mapping_file = os.environ["USER_MAP_PATH"]

def find_repo_issues(repo_name):
    gh = Github(gh_user, gh_pass)
    repo = gh.get_repo(repo_name)
    open_issues = repo.get_issues(state='open')
    return open_issues


# todo : efficiency
def lookup_ch_user(owner):
    f = open(user_mapping_file)
    ghu_to_chu = json.load(f)
    if (owner in ghu_to_chu):
        return ghu_to_chu[owner]
    else:
        return gh_user



# extract the comments from github and create clubhouse compatible
# comment mappings.  Map the comment owner id, otherwise use the
# user calling the script.
def comments_gh_to_ch(issue):
    comments = issue.get_comments()
    for c  in comments:
        print ("---\n" , c.body, "\n-----\n")
    return "todo"

# get labels from github but discard labels that apply to project and
# type.
def get_labels(issue):
    return "todo"

# Try to map the owner ids from github to clubhouse.
def get_owner_ids(issue):
    return "todo"

# make a best guess at the desired project_id based on the github
# labels.
def get_project_id(issue):
    return "todo"

def get_story_type(issue):
    return "todo"

def get_workflow_state(issue):
    return "todo"

# map a github issue to a clubhouse story.
def issue_to_story(issue):
    print(issue)
    story = {
        "comments": get_comments(issue),
        "created_at": issue.created_at,
        "description" : issue.body,
        "external_id" : issue.url.replace("api.github.com/repos/", "github.com/"),
        "labels" : get_labels(issue),
        "name" : issue.title,
        "owner_ids" : get_owner_ids(issue),
        "project_id" : get_project_id(issue),
        "requested_by_id" : lookup_ch_user(issue.user),
        "story_type" : get_story_type(issue),
        "updated_at" : issue.updated_at,
        "workflow_state" : get_workflow_state(issue)
    }
    return story

def main():
    ois = find_repo_issues("Yuneec/Firmware")
    iss = ois[0]
    story = issue_to_story(iss)
    pprint.pprint(story)


#    story = issue_to_story(ois[0])



if __name__ == '__main__':
    main()
