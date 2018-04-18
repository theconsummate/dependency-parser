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
    
    def print_conll_format(self):
        return str(self.id) + "\t" + self.form + "\t" + self.lemma + "\t" + self.upos + "\t" + self.xpos + "\t" + self.feats + "\t" + str(self.head) + "\t" + self.deprel + "\t" + self.deps + "\t" + self.misc
    
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
    
    def print_conll_format(self):
        string = ""
        for token in self.tokens[1:]:
            string += token.print_conll_format() + "\n"
        return string.strip()


class State():
    """
    n is the size of the sentence including the root
    """
    def __init__(self, n):
        self.n = n
        self.heads = [None] * (n)
        self.labels = [None] * (n)
        self.lefts = []
        self.rights = []
    

    def __add__(self, head, child, label=None):
        self.heads[child] = head
        self.labels[child] = label
    
    
    def doShift():
        pass
    
    def addLeftArc(self, head, child, label=None):
        # head < child required
        if head > child:
            raise ValueError('State#addLeftArc: head index should be less than the child index')
        self.rights[head].append(child)
        self.__add__(self, head, child, label)
    
    def addRightArc(self, head, child, label=None):
        # head > child required
        if head < child:
            raise ValueError('State#addRightArc: head index should be more than the child index')
        self.lefts[head].append(child)
        self.__add__(self, head, child, label)