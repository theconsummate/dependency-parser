# Statistical Dependency Parsing: Transition based Arc Standard Parser


## Source code
The code can be found at [github](https://github.com/theconsummate/dependency-parser) (https://github.com/theconsummate/dependency-parser)

## Introduction
I have implemented a transition based Arc Standard Parser trained on an averaged perceptron with greedy search. I trained two different models for English and German corpus separately using the same configurations (training method, feature set etc) and used them to parse the sentences for their respective languages.

The input/output file format was CoNLL06 having columns separated by tabs and sentences separated by blank line.

This report presents an outline of the implementation with brief descriptions of Class and method signatures. The full implementation can be seen in the source code as provided in the preceeding section.


## Sentence representation
The Sentence and Token classes are defined in the domain.py file. Each line in the input file is stored in a Token class which has the all the necessary attributes like id, form, upos, head and deprel. A Sentence has an array of Tokens.

```python

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
    ...

class Sentence():
    def __init__(self, tokens):
        self.tokens = tokens
    
    ...
```

## Maintaining the State
The domain.py file also has the State class which maintains the stack and the buffer at any given point during the parsing. All updates are done in place, so a single instance is sufficient.

At the beginning of a sentence, the stack and the buffer are initialized. If execution is in training mode, the gold heads are loaded otherwise, they are initialized to None.

The ``arc_standard_transition`` method applies a transition to modify the state and the ``get_gold_move_from_oracle`` queries the oracle to return a transition during the training phase.


## Feature Model
The features were calculated from the state variables and did not use the information about the previous (or next) transition. The following feature set was used:
```
Single token:
        s0.form + s0.upos, s0.form, s0.upos
        b0.form + b0.upos, b0.form, b0.upos
        b1.form + b1.upos, b1.form, b1.upos
        b2.form + b2.upos, b2.form, b2.upos

    # word pairs
    # S[0]-form,pos+B[0]-form,pos; S[0]-form,pos+B[0]-form;
    # S[0]-form+B[0]-form,pos; S[0]-form,pos+B[0]-pos;
    # S[0]-pos+B[0]-form,pos; S[0]-form+B[0]-form;
    # S[0]-pos+B[0]-pos; B[0]-pos+B[1]-pos;

Token pairs:
        s0.form + s0.upos + b0.form + b0.upos
        s0.form + s0.upos + b0.form
        s0.form + b0.form + b0.upos
        s0.form + s0.upos + b0.upos
        s0.upos + b0.form + b0.upos
        s0.form + b0.form
        s0.upos + b0.upos
        b0.upos + b1.upos

Three tokens:
        b0.upos + b1.upos + b2.upos
        b0.upos + b1.upos + s0.upos
```

## Machine Learning Method
#### Classes
The three different transitions, Right Arc, Left Arc and Shift are considered as the distinct classes for the model. At each state, the model predicts the best transition based on the features of the state.

#### Multi class Perceptron
The classifier.py file contains a Perceptron class which implements the basic perceptron algorithm. This does not perform very well as the accuracy on English dev set after 15 iterations of training was about 71%. This only increased marginally to 72% after 100 iterations. Since a perceptron is highly sensitive to recent updates, it is quite possible that the minor increase in accuracy is due to over fitting and not a result of additional learning.

Since there are three classes, the Multi class Perceptron consists of three perceptronsm. The class with the maximum score is considered to as the prediction.

#### Multi Class Averaged Perceptron
The AveragedPerceptron class in the classifier.py file implements the averaged perceptron algorithm. It is exactly similar to a Multi class Perceptron except the averaging step at the end. It stores a running sum of the weights and then at the end, the average_weights method averages all the weights before storing the model to disk.

This gives better performance as compared to Perceptron. I did not train the model for over 100 iterations as I believe that it will only lead to over-fitting, so the results can't be compared with Perceptron, but the results for 15 iterations should be enough to prove it's superior accuracy.

#### Training Loop
The train method in the train.py file implements the training loop. It iterates over all the sentences. For a given sentence, an empty state is initialized at the beginning and then the Oracle is queried to get the gold transition. This gold transition is considered as the gold class by the perceptron and updates are made accordingly. After this, the gold transition is applied to the state to reach the next state. This process continues until a terminal state has been reached, after which the loop moves over to the next sentence.

#### Greedy Search while Parsing
I have only implemented greedy search in this report. This is only relevant during the parsing phase when we already have a trained model and we need to output heads for a blind dataset. This is implemented in the ``parse`` method in the train.py file.

The transition having the maximum probability is selected and the state updates are made according to it, provided that sanity checks are not violated. For example, if the model says Left Arc but the first element on the stack is the ROOT token, then this transition is ignored. When either the Left Arc or Right Arc transition could not be performed, Shift is performed as default.

## Experimental results on dev data set.
The German model had an accuracy of 79.08 % while the English model had an accuracy of 81.67 %.