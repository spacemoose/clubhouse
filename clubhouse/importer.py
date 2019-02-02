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
def lookup_ch_user(gh_named_user):
    f = open(user_mapping_file)
    ghu_to_chu = json.load(f)
    name =gh_named_user.login
    if (name in ghu_to_chu):
        return ghu_to_chu[name]
    else:
        return gh_user


# create a clubhouse comment from a github issue.
# missing the story-public-id, which has to be added

def commment_from_issue(issue):
    return {
        "author_id":
        "created_at":
        "external_id":
        "text':issue.body",
        "updated_at":
        }

# extract tthe comments from github and create clubhouse compatible
# comment mappings.  Map the comment owner id, otherwise use the
# user calling the script.
def get_comments(issue):
    gh_comments = issue.get_comments()
    ch_comments = []
    for c  in gh_comments:
        ch_comments.append(c.body)
    return ch_comments

# get labels from github but discard labels that apply to project and
# type.
def get_labels(issue):
    return "todo"

# Try to map the owner ids from github to clubhouse.
def get_owner_ids(issue):
    owner_ids=[]
    for o in issue.assignees:
        owner_ids.append(lookup_ch_user(o))
    return owner_ids

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
    story = {
        "comments": get_comments(issue),
        "created_at": issue.created_at,
        "description" : issue.body,
        "external_id" : issue.html_url,
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

def passes_filter(issue):
    if issue.pull_request is None:
        return False
    for l in issue.labels:
        print (l.name)
        if l.name == "product":
            return False
    return True

def main():
    ois = find_repo_issues("Yuneec/Firmware")
    for i in ois :
        if passes_filter(i):
            story = issue_to_story(i)
            print (story["external_id"])
            pprint.pprint(story)
            break
#    story = issue_to_story(ois[0])



if __name__ == '__main__':
    main()
