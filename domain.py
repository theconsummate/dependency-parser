
SHIFT = 0; RIGHT = 1; LEFT = 2;
ACTIONS = (SHIFT, RIGHT, LEFT)
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
        try:
            self.head = int(items[6])
        except ValueError:
            self.head = None
        self.deprel = items[7]
        self.deps = items[8] # not in use
        self.misc = items[9] # not in use

    def __str__(self):
        return "{id=" + str(self.id) + ",form=" + self.form + ",head=" + str(self.head) + ",deprel=" + self.deprel + "}"

    def print_conll_format(self):
        # if not self.head:
        #     self.head = -1
        return str(self.id) + "\t" + self.form + "\t" + self.lemma + "\t" + self.upos + "\t" + self.xpos + "\t" + self.feats + "\t" + str(self.head) + "\t" + self.deprel + "\t" + self.deps + "\t" + self.misc

    @staticmethod
    def get_root_token():
        return Token("0\t<ROOT>\t<ROOT>\t<ROOT>\t_\t_\t-1\tROOT\t_\t_")

    @staticmethod
    def get_empty_token():
        return Token("-1\t<EMPTY>\t<EMPTY>\t<EMPTY>\t_\t_\t-1\tEMPTY\t_\t_")


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

    def set_heads(self, heads):
        if not len(heads) == len(self.tokens):
            raise ValueError('Sentence#set_heads: length of input heads array not equal to the number of tokens')
        for t, h in zip(self.tokens, heads):
            t.head = h


class State():
    """
    n is the size of the sentence including the root. 0 is the root index and after that is the sentence.
    """
    def __init__(self, n):
        self.n = n
        # init buffer with all tokens including root
        self.buffer = range(n)
        # pop the first root token
        self.buffer.pop(0)
        # init stack and add root token to it
        self.stack = [0]
        # arrays of size n for heads and labels
        self.heads = [None] * (n)
        self.labels = [None] * (n)
        self.lefts = [list() for x in range(n)]
        self.rights = [list() for x in range(n)]
        # add the head of root as -1
        self.heads[0] = -1


    """
    internal method, adds an arc to the state.
    """
    def __add__(self, head, dependent, label=None):
        self.heads[dependent] = head
        self.labels[dependent] = label

    """
    fills up the heads array. this should only be used during training to load the gold arcs.
    """
    def set_gold_heads(self, tokens):
        # set head of root token
        # self.heads[0] = -1
        # it is assumed that this tokens array does not have the root token
        for i in range(len(tokens)):
            self.heads[i] = tokens[i].head

    """
    pop the first element of the buffer and add it to the stack.
    """
    def shift(self):
        # buffer should have atleast 2 elements or stack is empty
        if len(self.buffer) < 1 and len(self.stack) > 0:
            raise ValueError('State#shift: buffer should have atleast 2 elements when stack is not empty')
        self.stack.append(self.buffer.pop(0))


    """
    adds a Left Arc
    """
    def addLeftArc(self, head, dependent, label=None):
        # arc is from head to dependent
        # head > dependent required
        if head < dependent:
            # print self.heads
            # print head
            # print dependent
            raise ValueError('State#addLeftArc: head index should be more than the dependent index')
        self.rights[head].append(dependent)
        self.__add__(head, dependent, label)


    """
    adds a right Arc
    """
    def addRightArc(self, head, dependent, label=None):
        # arc is from head to dependent
        # head < dependent required
        if head > dependent:
            raise ValueError('State#addRightArc: head index should be less than the dependent index')
        self.lefts[head].append(dependent)
        self.__add__(head, dependent, label)


    """
    A function to check, whether a token has collected all its dependents before it is assigned as a right dependent of another token.
    Only used during training while determining the next correct transition from oracle.
    """
    def has_all_children(self, buffer_top):
        if buffer_top in [self.heads[index] for index in self.buffer]:
            return False
        return True


    """
    An Arc Standard Oracle, Joakim and Nivre
    """
    def arc_standard_oracle(self, stack_top, buffer_top):
        if self.heads[stack_top] == buffer_top:
            return LEFT
        elif self.heads[buffer_top] == stack_top and self.has_all_children(buffer_top):
            return RIGHT
        else:
            return SHIFT


    """
    Performs sanity checks, queries the oracle and returns the next transition.
    """
    def get_gold_move_from_oracle(self):
        if len(self.stack) == 0:
            return SHIFT
        return self.arc_standard_oracle(self.stack[-1], self.buffer[0])


    """
    Applies a given transition to this state object.
    """
    def arc_standard_transition(self, action):
        # print "transtition ############ " + str(action)
        if action == LEFT:
            # pop the first element of buffer and add an arc.
            if self.stack[-1] == 0:
                # top of stack is root
                # raise ValueError("State#arc_standard_transition:top of stack is root, can not create left arc")
                # do shift instead
                self.shift()
            # elif self.stack[-1] < self.buffer[0]:
            #     # head is less than dependent
            #     self.shift()
            else:
                self.addLeftArc(self.buffer[0], self.stack.pop())
        elif action == RIGHT:
            # pop the last element of stack and first element of the buffer and add an arc.
            if not (len(self.stack) > 0 and len(self.buffer) > 0):
                self.shift()
            stack_top = self.stack.pop()
            self.addRightArc(stack_top, self.buffer.pop(0))
            # add the stack_top to the first position in the buffer
            self.buffer.insert(0, stack_top)
        else:
            self.shift()


    """
    determines whether the current state is terminal or not/
    """
    def is_terminal(self):
        if len(self.buffer) == 0:
            return True
        return False
