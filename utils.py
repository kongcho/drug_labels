import csv

def get_first_row(fin):
    arr = []
    with open(fin, "r") as f:
        r = csv.reader(f, delimiter=",", skipinitialspace=True)
        for row in r:
            arr.append(row[0])
    return arr

if __name__ == "__main__":
    pass
