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
    # f means form and p means pos
    if s0:
        features['s0_f_p=%s' % (s0.form + s0.upos)] = 1
        features['s0_f=%s' % s0.form] = 1
        features['s0_p=%s' % s0.upos] = 1
    if b0:
        features['b0_f_p=%s' % (b0.form + b0.upos)] = 1
        features['b0_f=%s' % b0.form] = 1
        features['b0_p=%s' % b0.upos] = 1
    if b1:
        features['b1_f_p=%s' % (b1.form + b1.upos)] = 1
        features['b1_f=%s' % b1.form] = 1
        features['b1_p=%s' % b1.upos] = 1
    if b2:
        features['b2_f_p=%s' % (b2.form + b2.upos)] = 1
        features['b2_f=%s' % b2.form] = 1
        features['b2_p=%s' % b2.upos] = 1
    

    # word pairs
    # S[0]-form,pos+B[0]-form,pos; S[0]-form,pos+B[0]-form;
    # S[0]-form+B[0]-form,pos; S[0]-form,pos+B[0]-pos;
    # S[0]-pos+B[0]-form,pos; S[0]-form+B[0]-form;
    # S[0]-pos+B[0]-pos; B[0]-pos+B[1]-pos;

    if s0 and b0:
        features['s0_f_p+b0_f_p=%s' % (s0.form + s0.upos + b0.form + b0.upos)] = 1
        features['s0_f_p+b0_f=%s' % (s0.form + s0.upos + b0.form)] = 1
        features['s0_f+b0_f_p=%s' % (s0.form + b0.form + b0.upos)] = 1
        features['s0_f_p+b0_p=%s' % (s0.form + s0.upos + b0.upos)] = 1
        features['s0_p+b0_f_p=%s' % (s0.upos + b0.form + b0.upos)] = 1
        features['s0_f_p+b0_f=%s' % (s0.form + b0.form)] = 1
        features['s0_p+b0_p=%s' % (s0.upos + b0.upos)] = 1
        
        # add three words
        features['b0_p+b1_p+b2_p=%s' % (b0.upos + b1.upos + b2.upos)] = 1

    if b0 and b1:
        features['b0_p+b1_p=%s' % (b0.upos + b1.upos)] = 1

    # three words
    # B[0]-pos+B[1]-pos+B[2]-pos; S[0]-pos+B[0]-pos+B[1]-pos;
    # h(S[0])-pos+S[0]-pos+B[0]-pos; S[0]-pos+ld(S[0])-pos+B[0]-pos;
    # S[0]-pos+rd(S[0])-pos+B[0]-pos; S[0]-pos+B[0]-pos+ld(B[0])-pos;

    if b0 and b1 and b2:
        features['b0_p+b1_p+b2_p=%s' % (b0.upos + b1.upos + b2.upos)] = 1
    
    if b0 and b1 and s0:
        features['b0_p+b1_p+s0_p=%s' % (b0.upos + b1.upos + s0.upos)] = 1

    return features

