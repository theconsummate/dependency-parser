import argparse
import io
from domain import State
from features import extract_features
from classifier import Perceptron

SHIFT = 0; RIGHT = 1; LEFT = 2;
ACTIONS = (SHIFT, RIGHT, LEFT)

def train(sentences):
    # init Perceptron
    perceptron = Perceptron(ACTIONS)

    print("training starting...")

    for sentence in sentences:
        # number of tokens in the sentence
        n = len(sentence.tokens)
        state = State(n)
        # set the gold heads
        # skip the root token while calling this function.
        print("setting gold heads")
        state.set_gold_heads(sentence.tokens[1:])
        # keep looping till parsing is complete

        while not state.is_terminal():
            features = extract_features(state, sentence.tokens)
            # get the next gold move
            gold = state.get_gold_move_from_oracle()
            # learn the next move for current state
            perceptron.learn(features, gold)
            # apply the gold move to get the new state
            state.arc_standard_transition(gold)


    # training is finished
    print("training finished")

    # save the model
    perceptron.save("model.pickle")
    print("model saved")


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

    train(sentences)
