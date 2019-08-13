# All of these examples assume you have successfully created an importer object.


#Return the story id associated with a github id.
def story_from_ghid():

# Returns True if the story is a PR.
def is_PR(story_id, imp):
    open_prs = imp.gh_repo.get_pulls(state='open')
    pr_ids = []
    for opr in open_prs:
        pr_ids.append(opr.number)
    if story_id in pr_ids:
        return True
    return False

# Returns False if the gh issue is a PR, or not open.
def needs_closing(story_id, issue_id, imp):
    if is_PR(story_id, imp):
        return False;
    ghi = imp.gh_repo.get_issue(issue_id)
    if ghi.state == 'open':
        return True


# Get a list of all open github issues.
# get a list of all created clubhouse issues.
# for each github issue, check if there is a corresponding ch issue.
# if there is, post a comment that it's been imported
    def close_imported_issues(imp):
    # create a dictionary of all ch stories with an external_id.
    imported_stories=dict()
    for story in imp.pych.stories:
    if story["external_id"] is not None:
        ghid=story["external_id"].split('/')[-1]
            print(ghid)
            imported_stories[int(ghid)] = story
    for story_by_ghid in imported_stories:
        if needs_closing(story_by_ghid, imported_stories[story_by_ghid]["id"], imp):
            print("gh: " + str(story_by_ghid) + " CH: " + str(imported_stories[story_by_ghid]["id"]))
