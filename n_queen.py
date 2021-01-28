# assignment csp=8 {*,*,*,*,*,*,*,*} * = col index = row
# ordering filtering structure
import random, time, math

def select_unassign_variable(assignment, csp):
    t = list(range(csp))
    t.sort(key = lambda x: abs(x-csp//2))
    for i in t:
        if i not in assignment:
            return i

def is_consistent(var, value, assignment, csp):
    # all values different
    # Xi-Xj != i - j
    # Xi-Xj != j - i
    if value in assignment.values():
        return False
    
    for i in range(csp):
        if i not in assignment:
            continue
        if i - var == assignment[i] - value:
            return False
        if var - i == assignment[i] - value:
            return False
    return True
    
def is_complete(assignment, csp):
    return len(assignment) == csp

def domain_values(var, assignment, csp, domains):
    if var in domains:
        random.shuffle(domains[var])
        return domains[var]
    else:
        t = list(range(csp))
        random.shuffle(t)
        domains[var] = t
        return domains[var]

def add(assignment, value, var):
    assignment[var] = value

def remove(assignment, value, var):
    if var in assignment:
        assignment.pop(var)

def backtrack(assignment, csp, domains, t):
    if time.time() - t > 0.5 * math.factorial(csp//100):
        return "tle"
    if is_complete(assignment, csp):
        return assignment
    var = select_unassign_variable(assignment, csp)
    for value in domain_values(var, assignment, csp, domains):
        if is_consistent(var, value, assignment, csp):
            add(assignment, value, var)
            result = backtrack(assignment, csp, domains, t)
            if result:
                return result
        remove(assignment, value, var)
    return {}

def conflicts(assignment, csp):

    def hits(assignment, csp, var, value):
        total = 0
        for i in range(csp):
                if i == var:
                        continue
                if assignment[i] == value or abs(i - var) == abs(assignment[i] - value):
                        total += 1
        return total

    return [hits(assignment, csp, var, assignment[var]) for var in range(csp)]


def n_queen(n, ot = None):
    t = time.time()
    if not ot:
        ot = t
    result = backtrack({}, n, {}, t)
    if result == "tle":
        return n_queen(n,ot)
    print("n =", n,":", result)
    if result:
        print("errors: ", sum(conflicts(result, n)))
    else:
        print("No solution")
        
    time_used = time.time()-ot
    print("time used:", time_used)
    return time_used
    
def n_queen_test(n):
    t_sum = 0
    for i in range(100):
        print("Trials: ", i+1)
        t_sum += n_queen(n, time.time())
        print()
    print("ave time:", t_sum/100)
    
n_queen_test(100)
