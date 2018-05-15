"""
convert state into features
"""
def extract_features(state, tokens):
    features = {}
    features['bias'] = 1

    # get s0, it's head, left dependent and right dependent if any
    s0 = None
    hs0 = None
    lds0 = None
    rds0 = None
    if len(state.stack) > 0:
        stack_index = state.stack[-1]
        s0 = tokens[stack_index]
        # check if the stack already has a head or not.
        if state.heads[stack_index]:
            hs0 = tokens[state.heads[stack_index]]
        # check for ld, take the first one if present
        if len(state.lefts[stack_index]) > 0:
            lds0 = tokens[state.lefts[stack_index][0]]
        # check for rd, take the first one if present
        if len(state.rights[stack_index]) > 0:
            rds0 = tokens[state.rights[stack_index][0]]

    # get buffer tokens
    b0 = None
    b1 = None
    b2 = None
    ldb0 = None

    if len(state.buffer) > 2:
        b0 = tokens[state.buffer[0]]
        b1 = tokens[state.buffer[1]]
        b2 = tokens[state.buffer[2]]
    elif len(state.buffer) > 1:
        b0 = tokens[state.buffer[0]]
        b1 = tokens[state.buffer[1]]
    elif len(state.buffer) > 0:
        b0 = tokens[state.buffer[0]]
    
    # add ldb0
    if b0:
        # check for ld, take the first one if present
        if len(state.lefts[state.buffer[0]]) > 0:
            ldb0 = tokens[state.lefts[state.buffer[0]][0]]

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

    if hs0 and s0 and b0:
        features['hs0_p+s0_p+b0_p=%s' % (hs0.upos + s0.upos + b0.upos)] = 1
    
    if lds0 and s0 and b0:
        features['lds0_p+s0_p+b0_p=%s' % (lds0.upos + s0.upos + b0.upos)] = 1
    
    if rds0 and s0 and b0:
        features['rds0_p+s0_p+b0_p=%s' % (rds0.upos + s0.upos + b0.upos)] = 1
    
    if ldb0 and s0 and b0:
        features['ldb0_p+s0_p+b0_p=%s' % (ldb0.upos + s0.upos + b0.upos)] = 1
    
    return features

