# dependency-parser

### How to run
The ``train.py`` contains the main method.

#### Arguments
##### Required
- '--train_file': the path to the input conll file, whether for training or parsing.
- '--model_file': the path to which the model must either be stored or loaded from

##### Optional:
- '--train_mode': training or parse mode. True means Training and False means Parsing. default=False (parsing)
- '--num_iters': number of training iterations, default=15

#### Sample runs
##### Training
```
python train.py --train_file "data/german/train/tiger-2.2.train.conll06" --model_file="full.german.model" --train_mode

or 

python train.py --train_file "data/german/train/tiger-2.2.train.conll06" --model_file="full.german.model" --train_mode --num_iters=10
```

##### Parsing
```
python train.py --train_file "data/german/dev/tiger-2.2.dev.conll06.blind" --model_file="full.german.model"
```

The parsed output is saved in the file ``out.conll`` in the working directory.

### References:
Urls or Webpages referred:

https://explosion.ai/blog/parsing-english-in-python

https://gist.github.com/syllog1sm/10343947

https://explosion.ai/blog/part-of-speech-pos-tagger-in-python

https://github.com/sloria/textblob-aptagger/blob/master/textblob_aptagger/_perceptron.py