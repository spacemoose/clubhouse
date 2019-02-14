import pyclub


def make_changeset(epicname):
    epic = pyclub.pyclub(f'epic:{epicname}')
    stories = list(filter(lambda s:
                          s['story_type'] != "chore", epic.stories))
    stories = sorted(stories, key=lambda k: k['story_type'])
    for s in stories:
        print(f'|{s["id"]: <6}|{s["story_type"]: <8}'
              f' |{pyclub.ghid(s): <6}|{s["name"]}|')
        print (f'|--+--+--+--|')


make_changeset("1.6")
