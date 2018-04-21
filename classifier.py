
"""
A perceptron classifier
"""
class Perceptron():
    def __init__(self, features_array = [], classes = None):
        self.classes = classes
        init_weights()

    """
    self.weight looks like {"SHIFT":{"f1":0.1, ...}, "LEFT":{...}, "RIGHT":{...}}
    """
    def init_weights(features_array, bias = 0.1):
        self.weights = {}
        for feature in features_array:
            for cl in self.classes:
                self.weights[cl][feature] = 0.1

    def update_weights(cl, features, add = True):
        for feature, value in features.items():
            if add:
                self.weights[cl][feature] += value
            else:
                self.weights[cl][feature] -= value

    """
    calculate dot product of given feature vector model with current weights.
    features is a dict of feature name and value
    """
    def predicted_class(features):
        classs = -1
        max_score = 0
        for cl in self.classes:
            sc = 0
            for feature, value in features.items():
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
        prediction = predicted_class(features)
        if not prediction == gold:
            update_weights(gold, features, True)
            update_weights(prediction, features, False)
