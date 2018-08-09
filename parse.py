from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re

class indication(object):
    def __init__(self):
        self.base_url = "https://www.uptodate.com"
        self.parser = "lxml"
        self.parse_rate = 1

        options = Options()
        options.add_argument("--headless")
        options.add_argument('--no-sandbox')
        options.add_argument('start-maximized')
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")
        try:
            self.driver = webdriver.Chrome(executable_path="./drivers/chromedriver", options=options)
            self.driver.implicitly_wait(30)
        except Exception as e:
            return self._setup_error("can't connect to page: {0}".format(e.message), "")

    def _setup_error(self, error_str, name=""):
        self.error = error_str
        print("{0}: Error: {1}".format(error_str, name))
        return None

    def _get_regex_group(self, text, regex):
        p = re.compile(regex)
        m = p.search(text)
        word = m.groups()[0].strip()
        return word

    def _text_to_file(self, text, fout):
        with open(fout, "wb") as f:
            f.write(text)
        return 0

    def get_search_result(self, name):
        parse_url = "{0}/contents/search?search={1}".format(self.base_url, name)
        self.driver.get(parse_url)
        try:
            wait = WebDriverWait(self.driver, 5)
            box = wait.until(EC.presence_of_element_located((By.ID, "searchresults")))
            source = box.get_attribute("innerHTML").encode("utf-8")
        except Exception as e:
            return self._setup_error("can't parse search page: {0}".format(e.message, name))
        soup = BeautifulSoup(source, self.parser)
        results = soup.find_all("div", {"class": "search-result"})
        re_str = "\s*([^\(\)\:]+)\s?"
        for result in results:
            url = self.base_url + result.a["data-ng-href"]
            url_str = result.a.contents[0]
            if "drug information" in url_str.lower() and "patient" not in url_str.lower():
                drug_name = self._get_regex_group(url_str, re_str).strip()
                return drug_name, url
        for result in results:
            if result.span:
                url_str = result.span.contents[0]
                if "drug information" in url_str.lower() and "patient" not in url_str.lower():
                    drug_name = self._get_regex_group(url_str, re_str).strip()
                    url = self.base_url + result.ul.a["data-ng-href"]
                    return drug_name, url
        return self._setup_error("can't find drug", name)

    def get_indications(self, url, name):
        indications = []
        self.url = url
        self.driver.get(url)
        try:
            wait = WebDriverWait(self.driver, 5)
            box = wait.until(EC.presence_of_element_located((By.ID, "topicContent")))
            source = box.get_attribute("innerHTML").encode("utf-8")
        except Exception as e:
            return self._setup_error("can't parse indication page: {0}".format(e.message), name)
        soup = BeautifulSoup(source, self.parser)
        drug_info = soup.find("div", {"class": "block doa drugH1Div"})
        if not drug_info:
            parsed_name = name.replace("/", "_")
            parsed_name = parsed_name.replace(" ", "_")
            self._text_to_file(source, "./{0}_source.html".format(parsed_name))
            self.driver.get_screenshot_as_file("./{0}_screen.png".format(parsed_name))
            return self._setup_error("can't parse webpage: can't find information", name)
        dosages = drug_info.find_all("p", \
                                     {"style": re.compile("text-indent:-2em;margin-left:2em")}) \
                  + drug_info.find_all("p", \
                                       {"style": re.compile("text-indent:0em;display:inline")})
        uses_block = soup.find("div", {"class": "block use drugH1Div"})
        uses = []
        if uses_block:
            uses = uses_block.find_all("p", \
                                       {"style": re.compile("text-indent:-2em;margin-left:2em")}) \
                   + uses_block.find_all("p", \
                                         {"style": re.compile("text-indent:0em;display:inline")})
        symptoms = dosages + uses
        if not symptoms:
            parsed_name = name.replace("/", "_")
            parsed_name = parsed_name.replace(" ", "_")
            self._text_to_file(source, "./{0}_source.html".format(parsed_name))
            self.driver.get_screenshot_as_file("./{0}_screen.png".format(parsed_name))
            return self._setup_error("can't parse webpage: can't find indications", name)
        re_str = "\s*([^\(\)\:]+)\s?"
        for symptom in symptoms:
            if symptom.b:
                drug_str = symptom.b.contents[0]
                drug = self._get_regex_group(drug_str, re_str).strip()
                if drug.lower() not in ["note", "oral"] and drug not in indications:
                    indications.append(drug)
        return indications

    def get_drug_indications(self, name):
        result = self.get_search_result(name)
        if result is None:
            return None
        drug_name, url = result
        indications = self.get_indications(url, name)
        print("done with {0}".format(name))
        return [drug_name, indications]

    def close(self):
        return self.driver.close()

if __name__ == "__main__":
    pass
