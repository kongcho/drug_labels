from disease import disease, dic

import re
import csv
from fuzzywuzzy import fuzz

# Parse through list of indications
class fda_drug(object):
    def __init__(self, drug, indications):
        self.drug = drug
        self.unparsed_ind = indications
        self.data = []

    def _get_regex_group(self, text, regex):
        p = re.compile(regex)
        m = p.search(text)
        if not m:
            return None
        word = m.groups()[0].strip()
        return word

    def _parse_indications(self):
        remed = self.unparsed_ind.replace(", ", ";")
        remeds = remed.split(",")
        parsed_inds = []
        for med in remeds:
            parsed_inds.append(med.split(";")[0].strip())
        return parsed_inds

    def parse_indications(self):
        self.parsed_ind = self._parse_indications()

    def _calc_perc_match(self, base_word, input_word):
        total = len(base_word)
        perc = fuzz.token_sort_ratio(base_word, input_word)
        return perc

    def do_close_match(self, indication):
        self.params["perc_match"] = []
        arr = self.params["perc_match"]
        for candidate in self.parsed_ind:
            # if self._calc_perc_match(indication, candidate) == 100:
            #     print indication, candidate, self._calc_perc_match(indication, candidate)
            arr.append(self._calc_perc_match(indication, candidate))
        return 0

    def get_stats(self, indication):
        self.params = {}
        self.do_close_match(indication)
        return 0

    def get_best_result(self, param):
        arr = self.params[param]
        res = max(arr)
        i = arr.index(res)
        return res, self.parsed_ind[i], self.drug


class res_ind(object):

    def __init__(self, indication, data):
        self.indication = indication
        self.best_res = []
        self.data = data

    def match_database_cols(self, drug, drugs, dat, col_nos):
        try:
            i = drugs.index(drug)
        except Exception as e:
            print ("drug not found: %s" % drug)
            return [[]]*len(col_nos)
        arr = [dat[i][col] for col in col_nos]
        return arr

    def determine_matches(self, fda_drugs, drugs, dat, col_nos, match_limit=60):
        res = []
        for drug in fda_drugs:
            drug.get_stats(self.indication)
            res.append(drug.get_best_result("perc_match"))
        for r in res:
            result, best, drug = r
            extra = self.match_database_cols(drug, drugs, dat, col_nos)
            if result >= match_limit:
                self.best_res.append([best, result, drug] + extra)
        return 0

# Matches between indication and FDA drug, given indication
class match(object):
    def __init__(self):
        self.indications = []
        self.dates = []
        self.res = []

    def _setup_error(self, error_str, name=""):
        self.error = error_str
        print("Match Error: {0} - {1}".format(name, error_str))
        return None

    def _get_col(self, fin, col_no, skip_rows=0):
        arr = []
        with open(fin, "r") as f:
            for _ in range(skip_rows):
                next(f)
                r = csv.reader(f, delimiter=",", skipinitialspace=True)
            for row in r:
                arr.append(row[col_no])
        return arr

    def set_indications(self, fin):
        d = disease()
        dat = d.get_stata_database(fin)
        self.indications = d._lower_arr(d.get_database_indications(dat, "indication_new", True))
        return 0

    def get_fda_drugs(self, fin):
        arr = self._get_col(fin, 3, 1)
        self.fda_drugs = [fda_drug(drug) for drug in arr]
        return 0

    def _setup_match_stata(self, fin):
        dat = d.get_stata_database(fin)
        inds = d._lower_arr(d.get_database_indications(dat, "indication_new", False))
        return inds, dat

    def match_database_stata(self, indication, inds, dat, headers):
        d = disease()
        try:
            i = inds.index(indication)
        except Exception as e:
            return self._setup_error("indication not found", indication)
        arr = [d.get_database_indications(dat, head, False)[i] for head in headers]
        return arr

    def _setup_match_database(self, fin):
        d = disease()
        dat = d.get_csv_database(fin)
        inds = d._lower_arr(self._get_col(fin, 1, 1))
        return inds, dat

    def do_all_drugs(self, fda_drugs, fin, match_rate=60, col_nos=[], data_headers=[]):
        d = disease()
        drugs, dat = self._setup_match_database(fin)
        for ind in self.indications:
            # extra_data = self.match_database_stata(ind, inds, dat, data_headers)
            r = res_ind(ind, [])
            r.determine_matches(fda_drugs, drugs, dat, col_nos, match_rate)
            self.res.append(r)
        return 0

    def _format_res(self, fda_headers, stata_headers):
        whole = [["indication_new", "matched_indication", "score", "fda_drug"] + \
                 fda_headers + stata_headers]
        for r in self.res:
            for b in r.best_res:
                arr = [r.indication] + b + r.data
                whole.append(arr)
        return whole

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

if __name__ == "__main__":
    m = match()
    print m.match_database("vaginal atrophy", "./data/Indication_USA.dta", ["year", "month"])
