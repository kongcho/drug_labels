import textract
import re

class dict(object):
    def __init__(self, words=None, file_loc=None):
        if words is not None:
            self.words = words
        elif file_loc is not None:
            self.words = self._get_words(file_loc)

    def _get_words(self, file_loc):
        with open(file_loc) as f:
            return set(words.strip().lower() for word in file_loc)

    def check(self, word):
        return word.lower() in self.words

class pdf(object):
    def __init__(self, file_dir):
        self.text = textract.process(file_dir)
        print(self.text)

    def _get_sections(self):
        re_str = "\b\\n[A-Z[^a-zA-Z\d\s]]{2,}\b"

    def _get_indication_label(self):
        pass

    def get_indication(self, indication_text):
        pass

if __name__ == "__main__":
    file_dir = "./test/020164s085lbl.pdf"
    file_dir = "./data/FDA Generics Listing June 29 2018.pdf"
    pdf(file_dir)

    import enchant
    d = enchant.Dict("en_US")


"""
>>> re_str = "[A-Z||(^a-zA-Z\d)]{2,}"
>>> p = re.compile(re_str)
>>> p.findall(text)
['ACCURETIC', '(quinapril', 'HCl', 'hydrochlorothiazide)', 'Tablets', 'WARNING', 'FETAL', 'TOXICITY', 'When', 'pregnancy', 'is', 'detected', 'discontinue', 'ACCURETIC', 'as', 'soon', 'as', 'possible', 'Drugs', 'that', 'act', 'directly', 'on', 'the', 'renin', 'angiotensin', 'system', 'can', 'cause', 'injury', 'and', 'death', 'to', 'the', 'developing', 'fetus', 'See', 'Warnings', 'Fetal', 'Toxicity', 'DESCRIPTION', 'ACCURETIC', 'is', 'fixed', 'combination', 'tablet', 'that', 'combines', 'an', 'angiotensin', 'converting', 'enzyme', '(ACE)', 'inhibitor', 'quinapril', 'hydrochloride', 'and', 'thiazide', 'diuretic', 'hydrochlorothiazide', 'Quinapril', 'hydrochloride', 'is', 'chemically', 'described', 'as', '3S', '(R']
>>> re_str = "[A-Z][A-Z||(^a-zA-Z\d)]{2,}"
>>> p = re.compile(re_str)
>>> p.findall(text)
['ACCURETIC', 'HCl', 'Tablets', 'WARNING', 'FETAL', 'TOXICITY', 'When', 'ACCURETIC', 'Drugs', 'See', 'Warnings', 'Fetal', 'Toxicity', 'DESCRIPTION', 'ACCURETIC', 'ACE)', 'Quinapril']
>>> re_str = "[A-Z]{2,}[^a-zA-Z\d]*"
>>> p = re.compile(re_str)
>>> p.findall(text)
['ACCURETIC\xef\x83\x94\n\n(', 'HC', 'WARNING: ', 'FETAL ', 'TOXICITY\n\xef\x82\xb7\t ', 'ACCURETIC ', 'DESCRIPTION\n', 'ACCURETIC ', 'ACE) ']
>>> text
"b'ACCURETIC\xef\x83\x94\n\n(quinapril HCl/hydrochlorothiazide) Tablets\nWARNING: FETAL TOXICITY\n\xef\x82\xb7\t When pregnancy is detected, discontinue ACCURETIC as soon as possible.\n\xef\x82\xb7\t Drugs that act directly on the renin-angiotensin system can cause injury and death\nto the developing fetus. See Warnings: Fetal Toxicity\n\nDESCRIPTION\nACCURETIC is a fixed-combination tablet that combines an angiotensin-converting\nenzyme (ACE) inhibitor, quinapril hydrochloride, and a thiazide diuretic,\nhydrochlorothiazide.\nQuinapril hydrochloride is chemically described as [3S-[2[R*(R*)],"
>>> re_str = "\n[A-Z]{2,}[^a-zA-Z\d]*"
>>> p = re.compile(re_str)
>>> p.findall(text)
['\nWARNING: ', '\nDESCRIPTION\n']
>>> re_str = "[A-Z]{2,}[^a-zA-Z\d]*\n"
>>> p = re.compile(re_str)
>>> p.findall(text)
['ACCURETIC\xef\x83\x94\n\n', 'TOXICITY\n', 'DESCRIPTION\n']
>>> re_str = "[A-Z\s]{2,}[^a-zA-Z\d]*\n"
>>> p = re.compile(re_str)
>>> p.findall(text)
['ACCURETIC\xef\x83\x94\n\n', ' FETAL TOXICITY\n', '\n\nDESCRIPTION\n']
>>> re_str = "\n[A-Z\s]{2,}[^a-zA-Z\d]*\n"
>>> p = re.compile(re_str)
>>> p.findall(text)
['\n\nDESCRIPTION\n']
>>> re_str = "\n[A-Z]{2,}\s*[^a-zA-Z\d]*\n"
>>> p = re.compile(re_str)
>>> p.findall(text)
['\nDESCRIPTION\n']
>>> re_str = "[A-Z]{2,}\s*[^a-zA-Z\d]*\n"
>>> p = re.compile(re_str)
>>> p.findall(text)
['ACCURETIC\xef\x83\x94\n\n', 'TOXICITY\n', 'DESCRIPTION\n']
>>> re_str = "[A-Z]{2,}\s*[^a-zA-Z\d]*\n"


"""
