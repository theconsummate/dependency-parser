"""
An object containing the information about a single word in a sentence.
"""
class Token():
    delimiter = '\t'
    
    def __init__(self, line):
        items = line.split(self.delimiter)
        self.id = int(items[0])
        self.form = items[1]
        self.lemma = items[2]
        self.upos = items[3]
        self.xpos = items[4] # not in use
        self.feats = items[5] # not in use
        self.head = int(items[6])
        self.deprel = items[7]
        self.deps = items[8] # not in use
        self.misc = items[9] # not in use
    
    def __str__(self):
        return "{id=" + str(self.id) + ",form=" + self.form + ",head=" + str(self.head) + ",deprel=" + self.deprel + "}"
    
    @staticmethod
    def get_root_token():
        return Token("0\t<ROOT>\t<ROOT>\t<ROOT>\t_\t_\t-1\tROOT\t_\t_")


"""
A sentence has an array of Tokens
"""
class Sentence():
    def __init__(self, tokens):
        self.tokens = tokens
    
    def __str__(self):
        string = ""
        for token in self.tokens:
            string += str(token) + "\n"
        return string.strip()
