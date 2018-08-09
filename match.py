import pandas as pd
import csv
import re
from parse import indication

class disease(object):
    def __init__(self):
        pass

    def _format_arr(self, arr, sep=","):
        return sep.join(str(i) for i in arr)

    def _lower_arr(self, arr):
        return [x.lower() for x in arr]

    def _get_regex_group(self, text, regex):
        p = re.compile(regex)
        m = p.search(text)
        word = m.groups()[0].strip()
        return word

    def get_database_indications(self, fin):
        data = pd.io.stata.read_stata(fin)
        drugs = data["drugname"]
        parsed_drugs = []
        for line in drugs:
            result = line.split(" - ")
            parsed_drug = result[0].strip(" ")
            parsed_drugs.append(parsed_drug)
        uniques = list(set(parsed_drugs))
        return uniques

    def get_fda_drugs(self, fin):
        drugs = []
        re_str = "\s*\[\d+\]\s*([\x00-\x7F]+)"
        with open(fin, "r") as f:
            next(f)
            r = csv.reader(f, delimiter=",", skipinitialspace=True)
            for row in r:
                line = row[0].replace("\\n", " ")
                drug = self._get_regex_group(line, re_str)
                drugs.append(drug)
        return drugs

    def get_fda_indications(self, drugs):
        results = []
        failed = []
        i = indication()
        if i is None:
            failed.append([drug, i.error])
        for drug in drugs:
            result = i.get_drug_indications(drug)
            if result and result[1]:
                result[1] = self._format_arr(result[1])
                result = [drug] + result + [i.url]
                results.append(result)
                print result
            else:
                failed.append([drug, i.error])
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

if __name__ == "__main__":
    drug_names = ["accolate"]
    anita_dir = "./data/Indication_USA.dta"
    fda_dir = "./data/Generic Drug Indications.csv"
    d = disease()
    # data_drugs = d._lower_arr(d.get_database_indications(anita_dir))
    fda_drugs = d._lower_arr(d.get_fda_drugs(fda_dir))
    results, failed = d.get_fda_indications(fda_drugs)
    # results: [drug_name, indications]
    d._arr_to_csv_2d(results, "./results/indications.csv")
    # failed: ([da_drug_name, error_code]
    d._arr_to_csv_2d(failed, "./results/failed.csv")
