import argparse
import io
from domain import State
from features import extract_features
from classifier import Perceptron

SHIFT = 0; RIGHT = 1; LEFT = 2;
ACTIONS = (SHIFT, RIGHT, LEFT)

MODEL_FILENAME = "model.pickle"

NUM_ITERS = 10

def train(sentences):
    # init Perceptron
    perceptron = Perceptron(ACTIONS)

    print("training starting...")
    for i in range(NUM_ITERS):
        print("iteration : " + str(i))
        for sentence in sentences:
            # number of tokens in the sentence
            n = len(sentence.tokens)
            state = State(n)
            # set the gold heads
            # print("setting gold heads")
            state.set_gold_heads(sentence.tokens)
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
    perceptron.save(MODEL_FILENAME)
    print("model saved")


def parse(sentences):
    # load model
    perceptron = Perceptron(ACTIONS)
    perceptron.load(MODEL_FILENAME)

    for sentence in sentences[:10]:
        n = len(sentence.tokens)
        state = State(n)

        while not state.is_terminal():
            features = extract_features(state, sentence.tokens)
            # get action from model
            action = perceptron.predicted_class(features)
            # print action
            state.arc_standard_transition(action)
            print state.heads

        sentence.set_heads(state.heads)
    
    io.write_conll_file("out.conll", sentences)


def test(sentences):
    for sentence in sentences:
        print("learn the gold sequence of moves from the oracle")
        moves = []
        n = len(sentence.tokens)
        state = State(n)
        state.set_gold_heads(sentence.tokens)
        print "gold heads"
        print state.heads
        print (state.stack, state.buffer)
        while not state.is_terminal():
            gold = state.get_gold_move_from_oracle()
            moves.append(gold)
            state.arc_standard_transition(gold)
            print (state.stack, state.buffer)
            print state.heads
        print moves

        print "reset state and apply these moves"
        state = State(n)
        for move in moves:
            state.arc_standard_transition(move)
            print (state.stack, state.buffer)
            print state.heads
        # print state.heads




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_file', required=True)
    parser.add_argument('--train_mode', action="store_true", default=False)

    # parser.add_argument('-a', action="store_true", default=False)
    # parser.add_argument('-b', action="store", dest="b")
    # parser.add_argument('-c', action="store", dest="c", type=int)
    args = parser.parse_args()

    # for sentence in io.load_conll_file(args.train_file):
    #     print sentence.print_conll_format()
    #     print "---"
    sentences = io.load_conll_file(args.train_file)
    # io.write_conll_file("out.conll", sentences)

    if args.train_mode:
        train(sentences)
    else:
        # by default we will always parse
        parse(sentences)
    # test(sentences[:10])
