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

    m = match()
    m.set_indications(main_dat)

    # parse through database indications
    inds = m._get_col("./results/uptodate_indications.csv", 3, 1)
    fdas = m._get_col("./results/uptodate_indications.csv", 0, 1)
    dates = m._get_col("./results/uptodate_indications.csv", 1, 1)

    fda_drugs = []
    for i, drug in enumerate(fdas):
        f = fda_drug(drug, inds[i], dates[i])
        f.parse_indications()
        fda_drugs.append(f)

    # match indication with fda diseases
    headers = []
    m.do_all_drugs(long_dat, fda_drugs, headers)
    data = m._format_res(headers)
    m._arr_to_csv_2d(data, "./res.csv", True)
