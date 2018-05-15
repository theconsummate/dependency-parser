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

"""
Averaged perceptron classifier
"""
class AveragedPerceptron():
    def __init__(self, classes = None):
        self.classes = classes
        self.weights = {}
        # track these variables for (class, feature) pair
        self.accumulator = {}
        self.last_seen = {}
        
        # counter for instances seen
        self.i = 0
        
        # init the dicts 
        for cl in self.classes:
            self.weights[cl] = {}
            self.accumulator[cl] = {}
            self.last_seen[cl] = {}
        # init_weights(self)

    def update_weights(self, cl, features, add = True):
        for feature, value in features.items():
            # add this feature to our weights if it was not present before
            if feature not in self.weights[cl]:
                self.weights[cl][feature] = 0.1
            if feature not in self.accumulator[cl]:
                self.accumulator[cl][feature] = 0
            if feature not in self.last_seen[cl]:
                self.last_seen[cl][feature] = 0
            self.accumulator[cl][feature] += (self.i - self.last_seen[cl][feature]) * self.weights[cl][feature]
            self.last_seen[cl][feature] = self.i
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
            # increase the update counter
            self.i += 1
            self.update_weights(gold, features, True)
            self.update_weights(prediction, features, False)

    """
    call at the very end to average the weights.
    """
    def average_weights(self):
        for cl, features in self.weights.items():
            for feature, weight in features.items():
                acc = self.accumulator[cl].get(feature, 0)
                acc += (self.i - self.last_seen[cl].get(feature, 0)) * weight
                average = round(acc / float(self.i), 3)
                # update if there were no problems
                if average:
                    self.weights[cl][feature] = average

    
    def save(self, path):
        print "Saving model to %s" % path
        pickle.dump(self.weights, open(path, 'w'))


    def load(self, path):
        self.weights = pickle.load(open(path))