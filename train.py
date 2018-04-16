import argparse
import io


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_file', required=True)

    # parser.add_argument('-a', action="store_true", default=False)
    # parser.add_argument('-b', action="store", dest="b")
    # parser.add_argument('-c', action="store", dest="c", type=int)
    args = parser.parse_args()

    for sentence in io.load_conll_file(args.train_file):
        print sentence
        print "---"