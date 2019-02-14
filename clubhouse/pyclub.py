import requests
import config


# @todo: make a story class.

def ghid(story):
    """Given a story, extract a github id if one is present"""
    if "external_id" in story:
        eid = story["external_id"]
        if eid is None:
            return " "
        return eid[eid.rfind("/")+1:]



# I'm reqorking py_ch here a bit, hence the duplication.
# This should encompass just the interaction with clubhouse,
# github/clubhouse interaction can be handled elsewhere.
class pyclub:
    api_url = "https://api.clubhouse.io/api/v2"

    def __init__(self, query):
        self.stories = self.search_stories(query)
        self.user_ids = self.get_username_map()

    def get_username_map(self):
        """Get the map of login names to UUID.  """
        r = requests.get(self.api_url + "/members?token="
                         + config.clubhouse_token)
        members = dict()
        for m in r.json():
            members[m["profile"]["mention_name"]] = m["id"]
        return members

    def search(self, params):
        """ Return the response json if it was succsful, print diagnostics
        and return None if it failed"""
        ss_url = self.api_url+"/search/stories"
        r = requests.get(ss_url,  params=params)
        r.encoding = 'utf-8'
        if (r.status_code != 200):
            print("\n", r.status_code,
                  " was returned when trying to execute the query: ")
            print(r.url)
            return None
        return r.json()

    def search_stories(self, query):
        """Return a list of clubhouse stories that satisfies the passed query.
        Any string passed as a search term in the web interface should produce
        identical results here.  The returned stories are simple dictionaries
        omment consisting with field names as keys."""
        print("gathering clubhouse stories", end='', flush=True)
        params = {'query': query, 'token': config.clubhouse_token}
        data = self.search(params)
        if data is None:
            print(
                "\nNo data returned.  Something went wrong with the request.")
            return None
        if 'next' in data:
            nxt = data['next']
        retval = data['data']
        while nxt is not None:
            nxt = nxt[nxt.rfind("=")+1:]
            params = {'query': query,
                      'next': nxt,
                      'token': config.clubhouse_token}
            data = self.search(params)
            nxt = data['next']
            retval += data["data"]
            print(".", end='', flush=True)
        print(f"\ncollected {len(retval)} stories")
        return retval
