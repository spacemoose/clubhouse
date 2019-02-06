from github import Github
import json
from pprint import pprint
import requests
from py_ch import py_ch
import config


class importer:
    clubhouse_api_url = "https://api.clubhouse.io/api/v2/"

    def __init__(self, repo_name):
        """ this asssumes you have a config.py defined, which provides the
        necessary authentificationinformation, and user mapping."""

        # I didn't get token authentification to work quickly enough, hence
        # this hack:
        self.clubhouse_projects = self.init_projects()
        self.gh_repo = Github(config.gh_user,
                              config.gh_password).get_repo(repo_name)
        self.open_issues = self.gh_repo.get_issues(state='open')
        self.pych = py_ch()

    def init_projects(self):
        projects_url = self.clubhouse_api_url + "projects"
        r = requests.get(projects_url,
                         params={'token': config.clubhouse_token})
        clubhouse_projects = dict()
        for p in r.json():
            clubhouse_projects[p['name']] = p['id']
        return clubhouse_projects

    def lookup_ch_user(self, gh_named_user):
        name = gh_named_user.login
        if (name in config.user_mapping):
            return config.user_mapping[name]
        else:
            return config.gh_user

    def comment_from_gh(self, ghc):
        """Create a clubhouse comment from a a github comment."""
        return {
            "author_id": self.pych.user_ids[self.lookup_ch_user(ghc.user)],
            "created_at": ghc.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "external_id": ghc.html_url,
            "text": ghc.body,
            "updated_at": ghc.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

    def get_comments(self, issue):
        """extract tthe comments from github and create clubhouse compatible
        comment mappings.  Map the comment owner id, otherwise use the
        user calling the script."""
        ch_comments = []
        if (issue.user.login not in config.user_mapping):
            ch_comments.append({"text": "Issue created in Github by "
                                + issue.user.login})
        gh_comments = issue.get_comments()
        for c in gh_comments:
            ch_comments.append(self.comment_from_gh(c))
        return ch_comments

    def get_owner_ids(self, issue):
        """ Takes the list of issue assignees, and tries to create clubhouse
        owners from them."""
        owner_ids = []
        for o in issue.assignees:
            owner_ids.append(self.pych.user_ids[self.lookup_ch_user(o)])
        return owner_ids

    def get_story_type(self, issue):
        """ if it can't figure out the type from the tags,
        I assume it's  a bug..."""
        for l in issue.labels:
            if l.name == "bug":
                return "bug"
            if l.name == "crash":
                return "bug"
            if l.name == "critical":
                return "bug"
            if l.name == "enhancement":
                return "feature"
            if l.name == "cleanup & maintenance":
                return "chore"
        return "bug"

    def get_labels(self, issue):
        """Get an issues labels in a ch friendly format"""
        labels = []
        for l in issue.labels:
            labels.append({
                "color": l.color,
                "external_id": l.url,
                "name": l.name
            })
        labels.append({'name': 'github'})
        return labels

    def get_project_id(self, issue):
        for l in issue.labels:
            if l.name == "H520":
                return self.clubhouse_projects["h520"]
            if l.name == "V18S":
                return self.clubhouse_projects["v18"]
            if l.name == "H600":
                return self.clubhouse_projects["h600"]
        if "H520" in issue.body or "h520" in issue.body:
            return self.clubhouse_projects["h520"]
        if "v18" in issue.body or "V18" in issue.body:
            return self.clubhouse_projects["v18"]
        if "h600" in issue.body or "H600" in issue.body:
            return self.clubhouse_projects["H600"]
        return self.clubhouse_projects["Firmware imports"]

    def issue_to_story(self, issue):
        """Map a github issue to a clubhouse story. """
        story = {
            "external_id": issue.html_url,
            "comments": self.get_comments(issue),
            "created_at": issue.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "description": issue.body,
            "labels": self.get_labels(issue),
            "name": issue.title,
            "owner_ids": self.get_owner_ids(issue),
            "project_id": self.get_project_id(issue),
            "story_type": self.get_story_type(issue),
            "updated_at": issue.updated_at.strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        print("here's the story")
        pprint(story)
        return story

    def passes_filter(self, issue):
        if issue.pull_request is not None:
            return False
        for l in issue.labels:
            if l.name == "product":
                return False
        return True

    def create_in_clubhouse(self, story):
        pprint(story)
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        stories_url = self.clubhouse_api_url + "stories"
        + "?token=" + config.clubhouse_token
        print(stories_url)
        pprint(json.dumps(story))
        r = requests.post(stories_url, data=json.dumps(story), headers=headers)
        pprint(r.url)
        pprint(r.json())

    def import_issue(self, issue_id):
        """Takes a github issue and creates a clubhouse story."""
        issue = self.gh_repo.get_issue(issue_id)
        if (self.pych.get_by_issue(issue_id) is not None):
            print(f"The issue with id {issue_id} is already in clubhouse:")
            pprint(self.pych.get_by_issue(issue_id))
        else:
            self.create_in_clubhouse(self.issue_to_story(issue))


# just for testing
def main():
    imp = importer(config.default_repo)
    for iss in imp.open_issues:
        pprint(imp.issue_to_story(iss))


if __name__ == '__main__':
    main()
