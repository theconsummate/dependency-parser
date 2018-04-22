"""
convert state into features
"""
def extract_features(state, tokens):
    features = {}
    features['bias'] = 1

    # get s0
    s0 = None
    if len(state.stack) > 0:
        s0 = tokens[state.stack[-1]]

    # get buffer tokens
    b0 = None
    b1 = None
    b2 = None
    if len(state.buffer) > 2:
        b0 = tokens[state.buffer[0]]
        b1 = tokens[state.buffer[1]]
        b2 = tokens[state.buffer[2]]
    elif len(state.buffer) > 1:
        b0 = tokens[state.buffer[0]]
        b1 = tokens[state.buffer[1]]
    elif len(state.buffer) > 0:
        b0 = tokens[state.buffer[0]]

    # now we have s0, b0, b1, b2
    # add unigrams
    if s0:
        features['s0_form_upos=%s' % (s0.form + s0.upos)] = 1
        features['s0_form=%s' % s0.form] = 1
        features['s0_upos=%s' % s0.upos] = 1
    if b0:
        features['b0_form_upos=%s' % (b0.form + b0.upos)] = 1
        features['b0_form=%s' % b0.form] = 1
        features['b0_upos=%s' % b0.upos] = 1
    if b1:
        features['b1_form_upos=%s' % (b1.form + b1.upos)] = 1
        features['b1_form=%s' % b1.form] = 1
        features['b1_upos=%s' % b1.upos] = 1
    if b2:
        features['b2_form_upos=%s' % (b2.form + b2.upos)] = 1
        features['b2_form=%s' % b2.form] = 1
        features['b2_upos=%s' % b2.upos] = 1
    return features

