import sys
from github import Github
import os

# I couldn't get token authentification to work, hence this hack:
gh_user = os.environ["GITHUB_USER"]
gh_pass = os.environ["GITHUB_PASSWORD"]
gh_token = os.environ["GITHUB_TOKEN"]


def find_repo_issues(repo_name):
    gh = Github(gh_user, gh_pass)
    repo = gh.get_repo(repo_name)
    open_issues = repo.get_issues(state='open')
    return open_issues

def get_comments(issue):
    return "implement me"

def get_labels(issue):
    return "implement me"

# map a github issue to a clubhouse story.
def issue_to_story(issue):
    print(issue)
    story = {
        "comments": get_comments(issue),
        "created_at": issue.created_at,
        "description" : issue.body,
        "external_id" : issue.url,
        "labels" : get_labels(issue)

def main():
    ois = find_repo_issues("Yuneec/Firmware")
    story = issue_to_story(ois[0])



if __name__ == '__main__':
    main()
