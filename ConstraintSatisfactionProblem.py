# Author: Annabel Revers
# Date:   October 2021

from collections import deque
from copy import deepcopy

class ConstraintSatisfactionProblem:

    def __init__(self, variables, current_domains, constraints):
        self.variables = variables
        self.current_domains = current_domains
        self.constraints = constraints
    
    # backtracking search for constraint satisfaction problem
    def backtracking_search(self, mrv_on, deg_on, lcv_on, ac3_on):
        return self.recursive_backtracking({}, mrv_on, deg_on, lcv_on, ac3_on)  # initial assignment is empty

    # recusirely called helper for backtracking_search
    def recursive_backtracking(self, assignment, mrv_on, deg_on, lcv_on, ac3_on):

        # check if assignment is completes
        if self.is_complete(assignment):
            # search is complete
            return assignment

        # select unassigned variable
        var = self.select_unassigned_variable(assignment, mrv_on, deg_on)

        # loop through domain values
        for value in self.order_domain_values(assignment, var, lcv_on): 
            # check if value assignment would be consistent with current assignment given constraints
            if self.is_consistent(assignment, var, value):
                # add variable-value pair to the assignment
                assignment[var] = value
                # save copy of current_domains in case ac3 later fails
                current_domains_copy = deepcopy(self.current_domains)
                # update variable's value in current_domains
                self.current_domains[var] = [value]

                if ac3_on:  # ac3 inference to detect failure early
                    if self.ac3(): 
                        # recurse on updated assignmnet
                        result = self.recursive_backtracking(assignment, mrv_on, deg_on, lcv_on, ac3_on)
                        # check that result is not failure
                        if result:
                            return result
                else: # don't use ac3
                    # recurse on updated assignmnet
                    result = self.recursive_backtracking(assignment, mrv_on, deg_on, lcv_on, ac3_on)
                    # check that result is not failure
                    if result:
                        return result

                # assignment was a failure, time to remove variable from assignment and backtrack 
                del assignment[var]
                # restore current_domains to its previous state
                self.current_domains = current_domains_copy
                
        # no values satisfy all constraints, return failure
        return False

    # checks if assignment is complete
    def is_complete(self, assignment):
        if len(assignment) == len(self.variables):
            return True
        return False

    # returns domain values for a variable
    def order_domain_values(self, assignment, var, lcv_on):
        if lcv_on:   # use the least constraining value heuristic to order variable's domain values
            return self.lcv_heuristic(assignment, var)
        else:   # return variable's domain values in no particular order
            return self.current_domains[var]

    # selects unassigned variable
    def select_unassigned_variable(self, assignment, mrv_on, deg_on):
        if mrv_on:  # use min remaining value heuristic to select variable
            return self.mrv_heuristic(assignment, deg_on)
        else:   # choose first unassigned variable we find
            for var in self.variables:
                if var not in assignment:
                    return var
            return None
        
    # minimum remaining values heuristic chooses the variable with the fewest legal values
    def mrv_heuristic(self, assignment, deg_on):
        min_remaining_values = float('inf')

        # loop through all variables
        for var in self.variables:
            # check if variable is unassigned
            if var not in assignment:
                # get number of value options left for variable
                options_left = len(self.current_domains[var])
                # check if found fewer legal values
                if options_left <= min_remaining_values:
                    min_remaining_values = options_left
        
        # add all variable's with same lowest number of legal values left to list
        ties = []
        for var in self.variables:
            if var not in assignment:
                if len(self.current_domains[var]) == min_remaining_values:
                    ties.append(var)

        if deg_on:  # use degree heuristic to break the ties
            return self.degree_heuristic(assignment, ties)
        else:   # choose first variable we find
            return ties[0]

    # degree heuristic chooses the variable with the most constraints on remaining variables
    def degree_heuristic(self, assignment, ties):
        max_constraints = float('-inf')
        best_var = None

        # loop through all variables
        for var in ties:
            # check if variable is unassigned
            if var not in assignment:
                # get number of constraints variable has on remaining variables
                num_constraints = self.get_num_constraints(var)

                # see if we have new greatest number of constraints
                if num_constraints > max_constraints:
                    max_constraints = num_constraints
                    best_var = var
 
        return best_var

    # inference technique that checks arc consistency of binary constraints
    def ac3(self):
        arc_queue = deque()

        # copy all binary contraints into queue
        for constraint in self.constraints:
            arc_queue.append(constraint)

        while arc_queue:
            var1, var2 = arc_queue.popleft()
            # check if latest assignment created any inconsistencies
            if self.remove_inconsistent_values(var1, var2):
                # recheck all constraints involving var1 if any updates to it's current domain values
                for constraint in self.constraints:
                    if constraint[0] == var1:
                        arc_queue.append((constraint[1],var1))

        # check if any variable now has no more domain options 
        for var in self.current_domains:
            if not self.current_domains[var]:
                # if so we return failure
                return False
        
        return True 

    # helper for ac3 that checks for any inconsistencies from latest assignment
    def remove_inconsistent_values(self, var1, var2):
        removed = False

        # list of any inconsistent domain options that need to be deleted
        to_delete = []
        
        # loop through all var1's current domain options
            # check if there is some y in var2's domains that would make x consistent with it
        for x in self.current_domains[var1]:
            found_option = False
            # loop through all var2's current domain options
            for y in self.current_domains[var2]:
                # checks if x and y would be consistent assignments with constraints on var1 and var2
                if self.found_consistent(var1,var2,x,y):
                    found_option = True
            
            # did not find any y that would make var2 consistent with var1 should it be assigned x
            if not found_option:
                to_delete.append(x)
                removed = True
        
        # delete all inconsistent values from var1's current domain options
        for v in to_delete:
            self.current_domains[var1].remove(v)

        return removed