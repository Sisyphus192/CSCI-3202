
import functools
import random

def every(predicate, seq):
    """True if every element of seq satisfies predicate.
    >>> every(callable, [min, max])
    1
    >>> every(callable, [min, 3])
    0
    """
    for x in seq:
        if not predicate(x): return False
    return True

def argmin_random_tie(seq, fn):
    """Return an element with lowest fn(seq[i]) score; break ties at random.
    Thus, for all s,f: argmin_random_tie(s, f) in argmin_list(s, f)"""
    best_score = fn(seq[0]); n = 0
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score; n = 1
        elif x_score == best_score:
            n += 1
            if random.randrange(n) == 0:
                best = x
    return best

def count_if(predicate, seq):
    """Count the number of elements of seq for which the predicate is true.
    >>> count_if(callable, [42, None, max, min])
    2
    """
    f = lambda count, x: count + predicate(x)
    return functools.reduce(f, seq, 0)

class CSP():
    def __init__(self, vars_x, domains, neighbors, sun_postions, selected_plants, constraints):
        self.vars_x = vars_x
        self.domains = domains
        self.exhausted_domains = {}
        self.neighbors = neighbors
        self.sun_postions = sun_postions
        self.constraints = constraints
        self.selected_plants = selected_plants
        self.initial = {}
        self.curr_domains = None
        self.pruned = None
        self.nassigns = 0
        self.counter = 0

    def assign(self, var, val, assignment):
        """Add {var: val} to assignment; Discard the old value if any.
        Do bookkeeping for curr_domains and nassigns."""
        self.nassigns += 1
        assignment[var] = val
        self.selected_plants[val.name] -= 1
        if self.selected_plants[val.name] <= 0:
            for key in self.domains:
                if val in self.domains[key]:
                    self.domains[key].remove(val)
                    if key not in self.exhausted_domains:
                        self.exhausted_domains[key] = []
                    self.exhausted_domains[key].append(val)
        if self.curr_domains:
            if self.fc:
                self.forward_check(var, val, assignment)
            if self.mac:
                AC3(self, [(Xk, var) for Xk in self.neighbors[var]])

    def unassign(self, var, assignment):
        """Remove {var: val} from assignment; that is backtrack.
        DO NOT call this if you are changing a variable to a new value;
        just call assign for that."""
        if var in assignment:
            val = assignment[var]
            if self.curr_domains:
                self.curr_domains[var] = self.domains[var][:]
            del assignment[var]
            self.selected_plants[val.name] += 1
            if self.selected_plants[val.name] > 0:
                for key in self.exhausted_domains:
                    if val in self.exhausted_domains[key]:
                        self.exhausted_domains[key].remove(val)
                        self.domains[key].append(val) # only want to add back if it had been removed

    def nconflicts(self, var, val, assignment):
        "Return the number of conflicts var=val has with other variables."
        # Subclasses may implement this more efficiently
        def conflict(var2):
            val2 = assignment.get(var2, None)
            return val2 != None and not self.constraints(var, val, var2, val2, self.sun_postions)
        return len(list(filter(conflict, self.neighbors[var])))

    def forward_check(self, var, val, assignment):
        "Do forward checking (current domain reduction) for this assignment."
        if self.curr_domains:
            # Restore prunings from previous value of var
            for (B, b) in self.pruned[var]:
                self.curr_domains[B].append(b)
            self.pruned[var] = []
            # Prine any other B=b assignment that conflict with var=val
            for B in self.neighbors[var]:
                if B not in assignment:
                    for b in self.curr_domains[B][:]:
                        if not self.constraints(var, val, B, b, self.sun_postions):
                            self.curr_domains[B].remove(b)
                            self.pruned[var].append((B, b))

    def display(self, assignment):
        "Show a human-readable representation of the CSP."
        # Subclasses can print in a prettier way, or display with a GUI
        print('CSP: ', self, 'with assignment: ', assignment)

#______________________________________________________________________________
# CSP Backtracking Search

def backtracking_search(csp, mcv=False, lcv=False, fc=False, mac=False):
    """Set up to do recursive backtracking search. Allow the following options:
    mcv - If true, use Most Constrained Variable Heuristic
    lcv - If true, use Least Constraining Value Heuristic
    fc  - If true, use Forward Checking
    mac - If true, use Maintaining Arc Consistency.              [Fig. 5.3]
    >>> backtracking_search(australia)
    {'WA': 'B', 'Q': 'B', 'T': 'B', 'V': 'B', 'SA': 'G', 'NT': 'R', 'NSW': 'R'}
    """
    if fc or mac:
        csp.curr_domains, csp.pruned = {}, {}
        for v in csp.vars_x:
            csp.curr_domains[v] = csp.domains[v][:]
            csp.pruned[v] = []
    csp.mcv = mcv
    csp.lcv = lcv
    csp.fc = fc
    csp.mac = mac
    return recursive_backtracking({}, csp)

def recursive_backtracking(assignment, csp):
    """Search for a consistent assignment for the csp.
    Each recursive call chooses a variable, and considers values for it."""
    if sum(csp.selected_plants.values()) == 0:
        return assignment
    csp.counter +=1
    print("Search counter: ", csp.counter, end='\r')
    var = select_unassigned_variable(assignment, csp)
    for val in order_domain_values(var, assignment, csp):
        if csp.fc or csp.nconflicts(var, val, assignment) == 0:
            csp.assign(var, val, assignment)
            result = recursive_backtracking(assignment, csp)
            if result is not None:
                return result
        csp.unassign(var, assignment)
    return None

def select_unassigned_variable(assignment, csp):
    "Select the variable to work on next.  Find"
    if csp.mcv: # Most Constrained Variable
        unassigned = [v for v in csp.vars_x if v not in assignment]
        return argmin_random_tie(unassigned,
                                 lambda var: -num_legal_values(csp, var, assignment))
    else: # First unassigned variable
        for v in csp.vars_x:
            if v not in assignment:
                return v

def order_domain_values(var, assignment, csp):
    "Decide what order to consider the domain variables."
    if csp.curr_domains:
        domain = csp.curr_domains[var]
    else:
        domain = csp.domains[var][:]
    if csp.lcv:
        # If LCV is specified, consider values with fewer conflicts first
        key = lambda val: csp.nconflicts(var, val, assignment)
        domain.sort(lambda x, y: cmp(key(x), key(y)))
    while domain:
        yield domain.pop()

def num_legal_values(csp, var, assignment):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        return count_if(lambda val: csp.nconflicts(var, val, assignment) == 0,
                        csp.domains[var])

#______________________________________________________________________________
# Constraint Propagation with AC-3

def AC3(csp, queue=None):
    """[Fig. 5.7]"""
    if queue == None:
        queue = [(Xi, Xk) for Xi in csp.vars_x for Xk in csp.neighbors[Xi]]
    while queue:
        (Xi, Xj) = queue.pop()
        if remove_inconsistent_values(csp, Xi, Xj):
            for Xk in csp.neighbors[Xi]:
                queue.append((Xk, Xi))

def remove_inconsistent_values(csp, Xi, Xj):
    "Return true if we remove a value."
    removed = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if every(lambda y: not csp.constraints(Xi, x, Xj, y, csp.sun_postions),
                 csp.curr_domains[Xj]):
            csp.curr_domains[Xi].remove(x)
            removed = True
    return removed

#______________________________________________________________________________
# Min-conflicts hillclimbing search for CSPs

def min_conflicts(csp, max_steps=1000):
    """Solve a CSP by stochastic hillclimbing on the number of conflicts."""
    # Generate a complete assignement for all vars_x (probably with conflicts)
    current = {}
    csp.current = current
    for var in csp.vars_x:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    # Now repeapedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars_x(current)
        if not conflicted:
            return current
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    return None

def min_conflicts_value(csp, var, current):
    """Return the value that will give var the least number of conflicts.
    If there is a tie, choose at random."""
    return argmin_random_tie(csp.domains[var],
                             lambda val: csp.nconflicts(var, val, current))
