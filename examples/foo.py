# Goal 1 is to import open issues from github, without importing
# duplicates, and subject to certain filters.

import requests
url = "https://clubhouse.io/api/rest/v2"
data = requests.get(url).json
