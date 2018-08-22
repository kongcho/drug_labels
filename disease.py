import pandas as pd
import csv
import re
from parse import indication

# dictionary to parse list of indications
class dic(object):
    def __init__(self, words=None, file_loc="./dict/words.txt"):
        if words is not None:
            self.words = self._lower_arr(words)
        elif file_loc is not None:
            self.words = self._get_words(file_loc)

    def _get_words(self, file_loc):
        with open(file_loc, "r") as f:
            return [word.strip().lower() for word in f]

    def _lower_arr(self, arr):
        return [x.lower() for x in arr]

    def check(self, word):
        return word.lower() in self.words

    def remove_words_from_dict(self, remove_words):
        for word in remove_words:
            if self.check(word):
                self.words.remove(word)
        print("Dict: removed all words from dict")
        return 0

    def print_dict(self, fout, words=None):
        if words is None:
            words = self.words
        with open(fout, "wb") as f:
            w = csv.writer(f, delimiter=",", lineterminator="\n")
            for word in words:
                w.writerow([word])
        print("Dict: printed dict")
        return 0

# get drugs/indications from STATA database
class disease(object):
    def __init__(self):
        pass

    def _setup_error(self, error_str, name=""):
        self.error = error_str
        print("Disease Error: {0} - {1}".format(name, error_str))
        return None

    def _format_arr(self, arr, sep=","):
        return sep.join(str(i) for i in arr)

    def _lower_arr(self, arr):
        return [x.lower() for x in arr]

    def _get_regex_group(self, text, regex):
        p = re.compile(regex)
        m = p.search(text)
        word = m.groups()[0].strip()
        return word

    def get_stata_database(self, fin):
        return pd.io.stata.read_stata(fin)

    def get_csv_database(self, fin):
        with open(fin, "rb") as f:
            r = csv.reader(f, delimiter=",")
            data = list(r)
        return data

    def get_database_indications(self, data, heading, get_uniques=True):
        drugs = data[heading]
        parsed_drugs = []
        for line in drugs:
            if heading == "drugname":
                result = line.split(" - ")
                parsed_drug = result[0]
            elif heading == "indication_new":
                parsed_drug = line.strip(" ")
            else:
                parsed_drug = line
            parsed_drugs.append(parsed_drug)
        if get_uniques:
            return list(set(parsed_drugs))
        return parsed_drugs

    def get_fda_drugs(self, fin, col_no=0):
        drugs = []
        re_str = "\s*\[\d+\]\s*([\x00-\x7F]+)"
        with open(fin, "r") as f:
            next(f)
            r = csv.reader(f, delimiter=",", skipinitialspace=True)
            for row in r:
                line = row[col_no].replace("\\n", " ")
                drug = self._get_regex_group(line, re_str)
                drugs.append(drug)
        return drugs

    def get_fda_indications(self, drugs, find, ffail):
        results = []
        failed = []
        i = indication()
        if i is None:
            failed.append([drug, i.error])
        for icount, drug in enumerate(drugs):
            result = i.get_drug_indications(drug)
            if result and result[1]:
                result[1] = self._format_arr(result[1])
                result = [drug] + result + [i.url]
                results.append(result)
                d._arr_to_csv_2d([result], find, False)
            else:
                fails = [drug, i.error]
                failed.append(fails)
                d._arr_to_csv_2d([fails], ffail, False)
        return results, failed

    def _arr_to_csv_2d(self, arr, fout, replace=True):
        if replace:
            op = "wb"
        else:
            op = "ab"
        with open(fout, op) as f:
            w = csv.writer(f, delimiter=",", lineterminator="\n")
            for row in arr:
                w.writerow(row)
        return 0

    def get_first_row(self, fin):
        arr = []
        with open(fin, "r") as f:
            r = csv.reader(f, delimiter=",", skipinitialspace=True)
            for row in r:
                arr.append(row[0])
        return arr
