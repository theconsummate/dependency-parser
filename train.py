import argparse
from domain import Token, Sentence, State
from features import extract_features
from classifier import Perceptron, AveragedPerceptron

SHIFT = 0; RIGHT = 1; LEFT = 2;
ACTIONS = (SHIFT, RIGHT, LEFT)

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


def write_conll_file(file, sentences):
    f = open(file, 'w')
    for sentence in sentences:
        f.write(sentence.print_conll_format() + "\n\n")
    f.close()


def train(sentences, num_iters, model_file):
    # init Perceptron
    # perceptron = Perceptron(ACTIONS)
    perceptron = AveragedPerceptron(ACTIONS)
    
    print("training starting...")
    for i in range(num_iters):
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

    # do average
    print("averaging...")
    perceptron.average_weights()

    # save the model
    perceptron.save(model_file)
    print("model saved")


def parse(sentences, model_file):
    # load model
    perceptron = Perceptron(ACTIONS)
    perceptron.load(model_file)

    for sentence in sentences:
        # print sentence
        n = len(sentence.tokens)
        state = State(n)

        while not state.is_terminal():
            # print state.stack
            # print state.buffer
            features = extract_features(state, sentence.tokens)
            # get action from model
            action = perceptron.predicted_class(features)
            # print action
            # print "####"
            # the action is just what the model says
            # apply it intelligently based on what the state is

            # if stack length is less than
            if action == SHIFT or len(state.stack) < 2:
                new_action = SHIFT
            elif action == LEFT and state.stack[-2] != -1:
                new_action = LEFT
            elif action == RIGHT and not(state.stack[-2] == -1 and len(state.buffer) != 0):
                new_action = RIGHT
            elif state.buffer_len() > 0:
                new_action = SHIFT
            else:
                new_action = RIGHT
            #
            # print new_action
            state.arc_standard_transition(new_action)
            # print state.heads

        sentence.set_heads(state.heads)

    write_conll_file("out.conll", sentences)


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
    parser.add_argument('--model_file', required=True)
    parser.add_argument('--train_mode', action="store_true", default=False)
    parser.add_argument('--num_iters', action="store", type=int, default=15)

    # parser.add_argument('-a', action="store_true", default=False)
    # parser.add_argument('-b', action="store", dest="b")
    # parser.add_argument('-c', action="store", dest="c", type=int)
    args = parser.parse_args()

    # for sentence in io.load_conll_file(args.train_file):
    #     print sentence.print_conll_format()
    #     print "---"
    sentences = load_conll_file(args.train_file)
    # io.write_conll_file("out.conll", sentences)

    if args.train_mode:
        train(sentences, args.num_iters, args.model_file)
    else:
        # by default we will always parse
        parse(sentences, args.model_file)
    # test(sentences[:10])
