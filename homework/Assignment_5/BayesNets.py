import unittest
import util
import random


## For the sake of brevity...
T, F = True, False

## From class:
def P(var, value, evidence={}):
    '''The probability distribution for P(var | evidence),
    when all parent variables are known (in evidence)'''
    if len(var.parents)==1:
        # only one parent
        row = evidence[var.parents[0]]
    else:
        # multiple parents
        row = tuple(evidence[parent] for parent in var.parents)
    return var.cpt[row] if value else 1-var.cpt[row]

## Also from class:
class BayesNode:

    def __init__(self, name, parents, values, cpt):
        if isinstance(parents, str):
            parents = parents.split()

        if len(parents)==0:
            # if no parents, empty dict key for cpt
            cpt = {(): cpt}
        elif isinstance(cpt, dict):
            # if there is only one parent, only one tuple argument
            if cpt and isinstance(list(cpt.keys())[0], bool):
                cpt = {(v): p for v, p in cpt.items()}

        self.variable = name
        self.parents = parents
        self.cpt = cpt
        self.values = values


    def __repr__(self):
        return repr((self.variable, ' '.join(self.parents)))

class BayesNet:
    '''Bayesian network containing only boolean-variable nodes.'''

    def __init__(self, nodes):
        '''Initialize the Bayes net by adding each of the nodes,
        which should be a list BayesNode class objects ordered
        from parents to children (`top` to `bottom`, from causes
        to effects)'''

        # kahn's algorithm for topological sorting
        self.nodes = []
        S = set([n for n in nodes if len(n.parents)==0]) #nodes with no parents

        while S:
            s = S.pop()
            self.nodes.append(s)
            S.update([m for m in nodes if set(m.parents).issubset([n.variable for n in self.nodes]) and m not in self.nodes])
        self.nodes.reverse()

    def add(self, node):
        '''Add a new BayesNode to the BayesNet. The parents should all
        already be in the net, and the variable itself should not be'''
        
        # check if variable already in net
        if node.variable not in [n.variable for n in self.nodes]:
            # check if parents are all present
            for p in node.parents:
                if set(node.parents).issubset([n.variable for n in self.nodes]):
                    self.nodes.append(node)
                    
    def find_node(self, var):
        '''Find and return the BayesNode in the net with name `var`'''
        # your code goes here...
        for n in self.nodes:
            if n.variable == var:
                return n


    def find_values(self, var):
        '''Return the set of possible values for variable `var`'''

        # your code goes here...
        for n in self.nodes:
            if n.variable == var:
                return n.values


    def __repr__(self):
        return 'BayesNet({})'.format(self.nodes)


def normalize(prob_distr):
    '''This is here to help'''
    total = sum(prob_distr)
    if total != 0:
        return map(lambda a: a / total, prob_distr)
    else:
        return prob_distr

def get_prob(Q, e, bn):
    '''Return probability distribution Q given evidence e in BayesNet bn
     e.g. P(Q|e). You may want to make helper functions here!'''

    QX = {}
    for qi in Q.values:
        e[Q.variable] = qi 
        QX[qi] = enumerate_all([n.variable for n in bn.nodes], e, bn)
    return list(normalize([QX[T],QX[F]]))

def enumerate_all(vars_, e, bn):
    if len(vars_) == 0:
        return 1.0
    Y = vars_.pop()
    if Y in e:
        val = P(bn.find_node(Y),e[Y], e) * enumerate_all(vars_, e, bn)
        vars_.append(Y)
        return val
    else:
        total = 0
        e[Y] = T
        total += P(bn.find_node(Y),T,e) * enumerate_all(vars_,e, bn)
        e[Y] = F
        total += P(bn.find_node(Y),F,e) * enumerate_all(vars_,e, bn)
        del e[Y]
        vars_.append(Y)
        return total

def make_Prediction(Q,e, bn):
    '''Return most likely value for variable Q given evidence e in BayesNet bn
     '''
    """Your Code Goes here"""
    prob = get_prob(Q, e, bn)
    return T if prob[0] > prob[1] else F


def prior_sample_n(bn, n):
    '''Return a list of samples from the BayesNet bn, where each sample is a dictionary
    Use Prior sampling (no evidence) to generate your samples, you will need
    to sample in the correct order '''

    """Your Code Goes here"""
    samples = []
    for i in range(n):
        e = {}
        for node in reversed(bn.nodes):
            pTrue = P(node, T, e)
            if random.random() <= pTrue:
                e[node.variable] = T
            else:
                e[node.variable] = F
        samples.append(e)

    return samples
