# Author: Annabel Revers
# Date:   October 2021

from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem

class MapProblem(ConstraintSatisfactionProblem):

    def __init__(self, states, colors, map):
        # human readbale problem information
        self.states = states
        self.colors = colors
        self.map = map  # contains all binary constaints on states

        # pass variables, current domains, and constraints to superclass
        super().__init__(self.states_to_ints(), self.make_current_domains(), self.make_constraints())
    
    # convert states to integers
    def states_to_ints(self):
        int_vars = []
        for i in range(len(self.states)):
            int_vars.append(i)
        return int_vars
    
    # generates a dictonary containing a list of value assignment options for each state
    def make_current_domains(self):
        current_domains = {}
        # start each state's list of domains as all possible colors
        for i in range(len(self.states)):
            options = []
            for j in range(len(self.colors)):
                options.append(j)
            current_domains[i] = options
        return current_domains

    # convert map constraints to integers constarints
    def make_constraints(self):
        int_constraints = []
        for constraint in self.map:
            int1 = self.states.index(constraint[0])
            int2 = self.states.index(constraint[1])
            int_constraints.append((int1, int2))
        return int_constraints
    
    # checks if value assignment for var would be consistent with current assignment
    def is_consistent(self, assignment, var, value):

        # loop through all constraints
        for constraint in self.constraints:
            # check if constraint involves var
            if constraint[0] == var:
                # check if neighbor is in assignment already
                if constraint[1] in assignment:
                    # check neighbor color
                    if assignment[constraint[1]] == value:
                        # found conflict, return false
                        return False
        
        # no conflict with current constraints, return true
        return True

    # gets the number of constraints a state has on remaining unassigned variables
    def get_num_constraints(self, var):
        # num constraints based on number of neighbors
        neighbors = 0
        for constraint in self.constraints:
            if constraint[0] == var:
                neighbors += 1
        return neighbors

    # least constraining value chooses the variable that rules out the least number of values
    def lcv_heuristic(self, assignment, var):
        # make array to keep track of number values each values rules out for its neighbors
        ruled_out_array = []
        for i in range(len(self.colors)):
            # make count of how many values this assignment would leave remaining
            remaining_values = 0
            # check constraints on neighbors assuming var is assigned this value
            for constraint in self.constraints:
                # look for neighbors
                if constraint[0] == var:
                    # check if neighbor is unassigned
                    if constraint[1] not in assignment:
                        # check if it still has this color as an option
                        if i in self.current_domains[constraint[1]]:
                            remaining_values += len(self.current_domains[constraint[1]])-1

            # add value and how many variables it leaves remaining to list
            ruled_out_array.append((i,remaining_values))
        
        # sort ruled out array of value/count pairs
        ruled_out_array.sort(key=lambda x:x[1])
        ruled_out_array.reverse()

        # get just the values
        ordered_domains = []
        for thing in ruled_out_array:
            ordered_domains.append(thing[0])

        return ordered_domains

    # helper for ac3's 'remove_inconsistent_values' function
        # checks if x and y would be consistent assignments with constraints on var1 and var2
    def found_consistent(self, var1, var2, x, y):
        return x!=y

    # converts assignment back to human-readable form and prints
    def print_assignment(self, assignment):
        for i in range(len(assignment)):
            print(self.states[i], "=", self.colors[assignment[i]])

# test code
if __name__ == "__main__":

    #########################################################################
    ################################ TESTS ##################################
    #########################################################################

    # variables are Australian territories
    variables = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
    # domain values are options for colors each territory can be
    domains = ["red", "green", "blue"]
    # constraints are which territories neighbor each other
    constraints = [("WA","NT"), ("WA","SA"), ("NT","WA"), ("NT","Q"), ("NT","SA"), ("Q","NT"), ("Q","NSW"), ("Q", "SA"), ("NSW", "Q"), ("NSW","V"), ("NSW","SA"), ("V","NSW"), ("V","SA"), ("SA","WA"), ("SA","NT"), ("SA","Q"), ("SA","NSW"), ("SA","V")]
    
    # TEST 1: test MapProblem with no heuristics
    print("----------------------------------------------")
    print("Testing MapProblem with no heuristics...")
    print("----------------------------------------------")
    mp1 = MapProblem(variables, domains, constraints)
    mp1.print_assignment(mp1.backtracking_search(False, False, False, False))
    print("----------")

    # TEST 2: test MapProblem with minimum remaining value heuristic
    print("----------------------------------------------")
    print("Testing MapProblem with mrv...")
    print("----------------------------------------------")
    mp2 = MapProblem(variables, domains, constraints)
    mp2.print_assignment(mp2.backtracking_search(True, False, False, False))
    print("----------")

    # TEST 3: test MapProblem with minimum remaining value and degree heuristics
    print("----------------------------------------------")
    print("Testing MapProblem with mrv and degree...")
    print("----------------------------------------------")
    mp3 = MapProblem(variables, domains, constraints)
    mp3.print_assignment(mp3.backtracking_search(True, True, False, False))
    print("----------")

    # TEST 4: test MapProblem with minimum remaining value, degree, and least constraining value heuristics
    print("----------------------------------------------")
    print("Testing MapProblem with mrv, degree, and lcv...")
    print("----------------------------------------------")
    mp4 = MapProblem(variables, domains, constraints)
    mp4.print_assignment(mp4.backtracking_search(True, True, True, False))
    print("----------")

    # TEST 5: test MapProblem with minimum remaining value, degree, and least constraining value heuristics as well as ac3
    print("----------------------------------------------")
    print("Testing MapProblem with mrv, degree, lcv, and ac3...")
    print("----------------------------------------------")
    mp4 = MapProblem(variables, domains, constraints)
    mp4.print_assignment(mp4.backtracking_search(True, True, True, True))
    print("----------")



  