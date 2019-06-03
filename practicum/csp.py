import random
import operator


class CSP:
    def __init__(self, variables, domains, adjacent_vars, constraints):
        self.variables = variables  # list of CSP variables
        self.domains = domains  # set of domains in the form var: [vals]
        self.adjacent_vars = (
            adjacent_vars
        )  # set of adjacent_vars for each variabe in the form var: [adjacent_vars]
        self.constraints = (
            constraints
        )  # set of contraints in the form of a function to be evaluated
        self.counter = (
            0
        )  # counts number of times backtrack is called, used only for performance analysis
        self.infered_assignments = None
        self.minimum_remaining_values = False
        self.degree_heuristic = False
        self.least_constraining_value = False

    # in the book is_consistent() only takes a variable and a value, but because we have
    # global constraints, we also need to pass assignment
    def is_consistent(self, variable, value, assignment):
        # checks for consistency with a given variable-value pair with all adjacent variable-vaue pairs
        for adj_variable in self.adjacent_vars[variable]:
            # if adjacent variable has not yet been assigned a value we don't worry about it
            if adj_variable in assignment:
                if not self.constraints(variable, value, adj_variable, assignment[adj_variable], assignment):
                    return False
        return True

    def is_complete(self, assignment):
        # standard CSP is complete when all variables have been assigned a value
        return len(assignment) == len(self.variables)


# backtacking_search(), backtrack(), AC_3(), and revise() were implemented
# directly from the pesudo-code in the book, chp. 6, where possible, some of
# the psuedo-code was very vague, e.g. SELECT-UNASSIGNED-VARIABLE(csp)
# only takes csp as an argument, but you cant check which variables have been assigned
# unless assignment is also passed
def backtracking_search(csp):
    return backtrack({}, csp)


def backtrack(assignment, csp):
    if csp.is_complete(assignment):
        return assignment, csp.counter
    csp.counter += 1
    if csp.counter > 100000: # we're not growing old age in this garden
        return None, csp.counter
    print("Backtrack counter: ", csp.counter, end="\r")
    variable = select_unassigned_variable(assignment, csp)
    for value in order_domain_values(variable, assignment, csp):
        if csp.is_consistent(variable, value, assignment):
            assignment[variable] = value
            #if AC_3(csp, variable, assignment): # I beleive this is the correct implementation for MAC
            result, cnt = backtrack(assignment, csp)
            if result is not None:
                return result, csp.counter
        if variable in assignment:
            del assignment[variable]
    return None, csp.counter


def select_unassigned_variable(assignment, csp):
    # choose the next unassigned variable in order
    unassigned = {}
    for variable in csp.variables:
        if variable not in assignment:
            unassigned[variable] = {"values": len(csp.domains[variable])}
    for variable in unassigned:
        # only *unassigned* variables count towards degree
        unassigned[variable]["degree"] = len([k for k in csp.adjacent_vars[variable] if k in unassigned])
    if csp.minimum_remaining_values and csp.degree_heuristic:
        mrv = {k:v for k,v in unassigned.items() if v["values"] == min(unassigned.values(), key=lambda x:x["values"])["values"]}
        dh =  [k for (k,v) in mrv.items() if v["degree"] == max(mrv.values(), key=lambda x:x["degree"])["degree"]]
        return random.choice(dh)
    elif csp.minimum_remaining_values:
        mrv = [k for k,v in unassigned.items() if v["values"] == min(unassigned.values(), key=lambda x:x["values"])["values"]]
        return random.choice(mrv)
    elif csp.degree_heuristic:
        dh = [k for k,v in unassigned.items() if v["degree"] == max(unassigned.values(), key=lambda x:x["degree"])["degree"]]
        return random.choice(dh)
        

    # randomizing the selected variable isnt necessary however, I want to measure performance
    # and this will get me different results each time
    return random.choice(list(unassigned.keys()))


def order_domain_values(variable, assignment, csp):
    # choose the next value in order
    # randomizing the selected value isnt necessary however, I want to measure performance
    # and this will get me different results each time
    if csp.least_constraining_value:
        lcv = []
        for value in csp.domains[variable]:
            conflict_count = 0
            for adj_variable in csp.adjacent_vars[variable]:
                # we're only concerned with not restricting adjacent unassigned variables
                if adj_variable not in assignment:
                    for adj_value in csp.domains[adj_variable]:
                        if not csp.constraints(variable, value, adj_variable, adj_value, assignment):
                            conflict_count += 1
            lcv.append((value, conflict_count))
        lcv.sort(key = operator.itemgetter(1))
        return [v[0] for v in lcv]
    
    random.shuffle(csp.domains[variable])
    return csp.domains[variable]

def inference(csp, variable, value):
    for var in csp.domains:
        if value in csp.domains[var]:
            csp.domains[var].remove(value)


def AC_3(csp, variable, assignment):
    # we start with only the arcs (Xj,Xi) for all Xj that are unassigned variables that are neighbors of Xi
    queue = [(variable_j, variable) for variable_j in csp.adjacent_vars[variable] if variable_j not in assignment]
    while queue:
        (variable_i, variable_j) = queue.pop() # remove first
        if revise(csp, variable_i, variable_j, assignment):
            if len(csp.domains[variable_i]) == 0:
                return False
            for variable_k in csp.adjacent_vars[variable_i]:
                if variable_k != variable_j:
                    # the variable is call queue is the pesudocode, but it is really a set
                    # so we're not concerened with order and just append it
                    queue.append((variable_k, variable_i))
        return True


def revise(csp, variable_i, variable_j, assignment):
    revised = False
    for value_x in csp.domains[variable_i]:
        if not all(
            csp.constraints(variable_i, value_x, variable_j, value_y, assignment)
            for value_y in csp.domains[variable_j]
        ):
            csp.domains[variable_i].remove(value_x)
            revised = True
    return revised
