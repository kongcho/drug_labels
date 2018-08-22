from disease import disease, dic
from match import match, fda_drug

# gets indications for fda drugs based to UpToDate
def get_indications():
    d = disease()

    fda_dir = "./data/Generic Drug Indications.csv"
    fda_drugs = d._lower_arr(d.get_fda_drugs(fda_dir))
    results, failed = d.get_fda_indications(fda_drugs, \
                                            "./results/indications.csv", "./results/failed.csv")
    d._arr_to_csv_2d(results, "./results/indications_all.csv")
    d._arr_to_csv_2d(failed, "./results/failed_all.csv")
    return 0

# removes drug/disease names from dictionary
def setup_dictionary():
    d = disease()
    anita_dir = "./data/Indication_USA.dta"
    data_drugs = d._lower_arr(d.get_database_indications(anita_dir, "drugname"))
    data_inds = d._lower_arr(d.get_database_indications(anita_dir, "indication_new"))

    dc = dic(None, "./dict/words.txt")
    dc.remove_words_from_dict(data_drugs)
    dc.print_dict("./dict/edit_words.txt", dc.words)
    return 0

if __name__ == "__main__":
    main_dat = "./data/Indication_USA_broad_narrow_states_subset_top15_OneDrugPerFirm.dta"
    long_dat = "./data/Indication_USA.dta"
    fda_dir = "./data/FDA Generics Listing June 29 2018.csv"

    m = match()
    m.set_indications(main_dat)

    # parse through database indications
    utd_inds = m._get_col("./results/uptodate_indications.csv", 2, 1)
    utd_drugs = m._get_col("./results/uptodate_indications.csv", 0, 1)

    drugs = []
    for i, drug in enumerate(utd_drugs):
        f = fda_drug(drug, utd_inds[i])
        f.parse_indications()
        drugs.append(f)

    # match indication with fda diseases
    fda_headers = ["dates"]
    col_nos = [5]
    stata_headers = []
    m.do_all_drugs(drugs, fda_dir, 60, col_nos, stata_headers)
    data = m._format_res(fda_headers, stata_headers)
    m._arr_to_csv_2d(data, "./res.csv", True)
