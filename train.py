import argparse
import io
from domain import State
from features import extract_features

def trainEach(sentence):
    # number of tokens in the sentence
    n = len(sentence.tokens)
    # add root element to the buffer
    buffer = [0]
    state = State(n)
    while stack or (i+1) < n:
        features = extract_features()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_file', required=True)

    # parser.add_argument('-a', action="store_true", default=False)
    # parser.add_argument('-b', action="store", dest="b")
    # parser.add_argument('-c', action="store", dest="c", type=int)
    args = parser.parse_args()

    # for sentence in io.load_conll_file(args.train_file):
    #     print sentence.print_conll_format()
    #     print "---"
    sentences = io.load_conll_file(args.train_file)
    # io.write_conll_file("out.conll", sentences)

    for sentence in sentences:
        trainEach(sentence)