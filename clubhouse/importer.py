import sys
from github import Github
import os
import json
import pprint
import requests
import ch_tools

clubhouse_api_url = "https://api.clubhouse.io/api/v2/"
clubhouse_token=os.environ['CLUBHOUSE_TOKEN']

# I didn't get token authentification to work quickly enough, hence
# this hack:
gh_user = os.environ["GITHUB_USER"]
gh_pass = os.environ["GITHUB_PASSWORD"]
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

def comment_from_gh(ghc): # ghc is github comment
    return {
        "author_id" : lookup_ch_user(ghc.user),
        "created_at" : ghc.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "external_id" : ghc.html_url,
        "text" : ghc.body,
        "updated_at" : ghc.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

# extract tthe comments from github and create clubhouse compatible
# comment mappings.  Map the comment owner id, otherwise use the
# user calling the script.
def get_comments(issue):
    ch_comments = []
    # okay, now it's getting silly, fix this
    f = open(user_mapping_file)
    usermap = json.load(f)
    name = issue.user.login
    if (name not in usermap):
        ch_comments.append({
            "text": "Issue created in Github by " + name
        })
    gh_comments = issue.get_comments()
    for c  in gh_comments:
        ch_comments.append(comment_from_gh(c))
    return ch_comments


# Try to map the owner ids from github to clubhouse.
def get_owner_ids(issue):
    owner_ids=[]
    for o in issue.assignees:
        owner_ids.append(lookup_ch_user(o))
    return owner_ids


# if it can't figure out the type from the tags, I assume it's  a bug...
def get_story_type(issue):
    for l in issue.labels:
        if l.name == "bug": return "bug"
        if l.name == "crash" : return "bug"
        if l.name == "critical" : return "bug"
        if l.name == "enhancement" : return "feature"
        if l.name == "cleanup & maintenance": return "chore"
    return "bug"


# get labels from github
def get_labels(issue):
    labels = []
    for l in issue.labels:
        labels.append({
            "color": l.color,
            "external_id": l.url,
            "name": l.name
        })
    labels.append({'name': 'github' })
    return labels


# Based on the labels, try to guess the project
# @todo I should really change this to a mapping...
def get_project_id(issue, projects):
    for l in issue.labels:
        if l.name == "H520": return projects["h520"]
        if l.name == "V18S": return projects["v18"]
        if l.name == "H600": return projects["h600"]
    if "H520" in issue.body or "h520" in issue.body: return projects["h520"]
    if "v18" in issue.body  or "V18"  in issue.body: return projects["v18"]
    if "h600" in issue.body or "H600" in issue.body: return projects["H600"]
    return projects["Firmware imports"]


def issue_to_story(issue, projects):
    """Map a github issue to a clubhouse story. """
    story = {
        "external_id" : issue.html_url,
        "comments": get_comments(issue),
        "created_at": issue.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "description" : issue.body,
        "labels" : get_labels(issue),
        "name" : issue.title,
        "owner_ids" : get_owner_ids(issue),
        "project_id" : get_project_id(issue, projects),
        "story_type" : get_story_type(issue),
        "updated_at" : issue.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    return story


def get_projects():
    projects_url = clubhouse_api_url + "projects"
    r = requests.get(projects_url,
                     params = {'token':clubhouse_token })
    projects = dict()
    for p in r.json():
        projects[p['name']] = p['id']
    return projects

def passes_filter(issue):
    if issue.pull_request is not None:
        return False
    for l in issue.labels:
        if l.name == "product":
            return False
    return True


def issues_to_stories(max_count):
    stories = []
    projects = get_projects()
    open_issues = find_repo_issues("Yuneec/Firmware")
    count = 0
    for i in open_issues :
        if passes_filter(i):
            stories.append(issue_to_story(i,projects))
            count +=1
            if count > max_count :
                 break
    return stories

# This exists to let me piece by piece test the creation of stories
def create_in_clubhouse(story):
    headers = {'Content-Type': 'application/json', 'Accept':'application/json'}
    stories_url = clubhouse_api_url+ "stories"+ "?token="+clubhouse_token
    print (stories_url)
    pprint.pprint(json.dumps(story))
    r = requests.post(stories_url, data=json.dumps(story), headers=headers)
    pprint.pprint(r.url)
    pprint.pprint(r.json())

def main():
    stories = issues_to_stories(0)
    for story in stories:
        create_in_clubhouse(story)


#    story = issue_to_story(ois[0])



if __name__ == '__main__':
    main()
