import json

from TwitterAPI import TwitterAPI
import config

SEARCH_TERM = "בחירות 2019"
if __name__ == '__main__':
    api = TwitterAPI(config.API_KEY, config.API_SECRET, auth_type='oAuth2')
    r = api.request('search/tweets', {'q': SEARCH_TERM, 'lang': 'he'})

    # for item in r:
    #     print(item['text'] if 'text' in item else item)
    with open("output.json", "w") as fileWriter:
        fileWriter.write(json.dumps(r.response.json()))
    print("Output written to file")

    exit(1)
