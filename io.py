from domain import Token, Sentence

def load_conll_file(file):
    f = open(file)
    sentences = []
    tokens = [Token.get_root_token()]
    for line in f.readlines():
        # remove the new line char first
        line = line.strip()
        if line == "":
            # the sentence has ended
            sentences.append(Sentence(tokens))
            tokens = [Token.get_root_token()]
        else:
            token = Token(line)
            tokens.append(token)
    return sentences