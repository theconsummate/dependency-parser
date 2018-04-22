import pickle
"""
A perceptron classifier
"""
class Perceptron():
    def __init__(self, classes = None):
        self.classes = classes
        self.weights = {}
        for cl in self.classes:
            self.weights[cl] = {}
        # init_weights(self)

    """
    self.weight looks like {"SHIFT":{"f1":0.1, ...}, "LEFT":{...}, "RIGHT":{...}}
    """
    # def init_weights(features_array, bias = 0.1):
    #     self.weights = {}
    #     for feature in features_array:
    #         for cl in self.classes:
    #             self.weights[cl][feature] = 0.1

    def update_weights(self, cl, features, add = True):
        for feature, value in features.items():
            # add this feature to our weights if it was not present before
            if feature not in self.weights[cl]:
                    self.weights[cl][feature] = 0.1
            if add:
                self.weights[cl][feature] += value
            else:
                self.weights[cl][feature] -= value

    """
    calculate dot product of given feature vector model with current weights.
    features is a dict of feature name and value
    """
    def predicted_class(self, features):
        classs = -1
        max_score = 0
        for cl in self.classes:
            sc = 0
            for feature, value in features.items():
                # add this feature to our weights if it was not present before
                if feature not in self.weights[cl]:
                    self.weights[cl][feature] = 0.1
                sc += self.weights[cl][feature] * value
            if classs == -1 or sc > max_score:
                max_score = sc
                classs = cl
        return classs


    """
    learns from a given feature instance
    features is a dict of features and their corresponding values.
    """
    def learn(self, features, gold):
        prediction = self.predicted_class(features)
        if not prediction == gold:
            self.update_weights(gold, features, True)
            self.update_weights(prediction, features, False)


    def save(self, path):
        print "Saving model to %s" % path
        pickle.dump(self.weights, open(path, 'w'))


    def load(self, path):
        self.weights = pickle.load(open(path))
