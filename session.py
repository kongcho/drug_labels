import requests

class session(object):
    def __init__(self, url):
        self.url = url

    def get(self, params=None, **kwargs):
        r = requests.get(self.url, params, **kwargs)
        if r.status_code != 200:
            logger.error("Requests failed, HTTP code: {0}".format(r.status_code))
        return r

if __name__ == "__main__":
    base_url = "https://dailymed.nlm.nih.gov/dailymed/services/"
    url = base_url + "drugnames"
    s = session(url)
    dic = {
        "drug_name": "ACTIVELLA"
    }
    r = s.get(dic)
    print(r.text)
    pass
