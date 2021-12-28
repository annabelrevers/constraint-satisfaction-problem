# Author: Annabel Revers
# Date:   October 2021

from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem

class CircuitBoardProblem(ConstraintSatisfactionProblem):

    def __init__(self, pieces, width, height):
        # human readable problem information
        self.pieces = pieces  # list of tuples containing pieces' width and height
        self.width = width  # board width
        self.height = height  # board height
        
        # used for printing result
        self.piece_to_char = self.make_piece_to_char() 

        # pass variable, current domains, and constraints to supersclass
        super().__init__(self.pieces_to_ints(), self.make_current_domains(), self.make_constraints())
    
    # convert pieces to integers
    def pieces_to_ints(self):
        variables = []
        for i in range(len(self.pieces)):
            variables.append(i)
        return variables

    # generates a dictionary containing each piece's list of possible assignment values
    def make_current_domains(self):
        current_domains = {}
        # start each piece's domain as all possible points in circuit board
        for i in range(len(self.pieces)):
            current_domains[i] = [] 
            for x in range(self.width):
                for y in range(self.height):
                    current_domains[i].append((x,y))    

        return current_domains

    # generates the binary constraints for each piece
    def make_constraints(self):
        constraints = []
        for i in range(len(self.pieces)):
            for j in range(len(self.pieces)):
                if i != j:
                    constraints.append((i, j))
        
        return constraints

    # generates dictionary mapping each piece variable to a specific character when printing result
    def make_piece_to_char(self):
        piece_to_char = {}
        letter = 97
        for piece in self.pieces:
            piece_to_char[piece] = chr(letter)
            letter += 1

        return piece_to_char
    
    # checks if value assignment for var would be consistent with current assignment
    def is_consistent(self, assignment, var, value):
        
        points = []
        piece = self.pieces[var]
        for x in range(value[0], value[0]+piece[0]):
            for y in range(value[1], value[1]+piece[1]):
                points.append((x,y))

        # check that nothing overlaps
        for var2 in assignment:

            mypoint = assignment[var2]
            piece2 = self.pieces[var2]
            for i in range(mypoint[0], mypoint[0]+piece2[0]):
                for j in range(mypoint[1], mypoint[1]+piece2[1]):
                    if (i, j) in points: 
                        #print("returning False")
                        return False

        if value[0]+piece[0] > self.width or value[1]+piece[1] > self.height:
            return False

        return True

    # gets the number of constraints a piece has on remaining unassigned variables
    def get_num_constraints(self, var):
        piece = self.pieces[var]
        # num constraints based on piece size
        return piece[0] * piece[1]

    # least constraining value chooses the variable that rules out the least number of values
    def lcv_heuristic(self, assignment, var):
        # make copy of domains for reordering
        value_counts = []

        # loop through variable's current domain optiosn
        for value in self.current_domains[var]:
            # get list of points piece would cover should it be placed at this value
            points_covered = []
            # get piece width,height tuple from dictionary
            piece = self.pieces[var]
            for x in range(value[0], value[0] + piece[0]):
                for y in range(value[1], value[1] + piece[1]):
                    points_covered.append((x,y))

            # loop through variable and see how many points this assignment would elimate from other piece
            count = 0
            for v in self.variables:
                if v not in assignment and not v == var:
                    for loc in points_covered:
                        if loc in self.current_domains[v]:
                            count += 1

            # append value and its count to array if consistent
            if self.is_consistent(assignment,var,value):
                value_counts.append((value,count))

        # sort value/count pairs
        value_counts.sort(key=lambda x:x[1])

        # get just the values to return
        domains = []
        for v in value_counts:
            domains.append(v[0])

        return domains

    # helper for ac3's 'remove_inconsistent_values' function
        # checks if x and y would be consistent assignments with constraints on var1 and var2
    def found_consistent(self, var1, var2, x, y):
        # get piece for var1
        piece1 = self.pieces[var1]

        # append all points that piece1 would occupy should it be assigned point y
        points = []
        for i in range(x[0], x[0]+piece1[0]):
            for j in range(x[1], x[1]+piece1[1]):
                points.append((i,j))

        # get piece for var2
        piece2 = self.pieces[var2]
        # loop through all points that piece2 would occupy should it be assigned point y 
        for i in range(y[0], y[0]+piece2[0]):
            for j in range(y[1], y[1]+piece2[1]):
                # if it occupies a point that piece1 does, then there is a conflict/inconsistency
                if (i, j) in points:
                    return False

        return True

    # prints final board assignment
    def print_board(self, assignment):

        # create empty board
        board = []
        for x in range(self.height):
            row = []
            for y in range(self.width):
                row.append(".")
            board.append(row)

        # add all pieces to board
        for var in assignment:
            piece = self.pieces[var]
            for x2 in range(assignment[var][0], assignment[var][0] + piece[0]):
                for y2 in range(assignment[var][1], assignment[var][1] + piece[1]):
                    board[self.height-y2-1][x2] = self.piece_to_char[piece]
        
        # print board
        for row in board:
            for thing in row:
                print(thing, end="")
            print("\n", end="")
    
# test code
if __name__ == "__main__":

    #########################################################################
    ################################ TESTS ##################################
    #########################################################################

    #TEST 1: test CircuitBoardProblem with no heuristics
    print("----------------------------------------------")
    print("Testing CircuitBoardProblem with no heuristics...")
    print("----------------------------------------------")
    cb1 = CircuitBoardProblem([(3,2),(5,2),(2,3),(7,1)],10,3)
    cb1.print_board(cb1.backtracking_search(False, False, False, False))
    print("----------")

    # # TEST 2: test CircuitBoardProblem with minimum remaining value heuristic
    print("----------------------------------------------")
    print("Testing CircuitBoardProblem with mrv...")
    print("----------------------------------------------")
    cb2 = CircuitBoardProblem([(3,2),(5,2),(2,3),(7,1)],10,3)
    cb2.print_board(cb2.backtracking_search(True, False, False, True))
    print("----------")

    # # TEST 3: test CircuitBoardProblem with minimum remaining value and degree heuristics
    print("----------------------------------------------")
    print("Testing CircuitBoardProblem with mrv and degree...")
    print("----------------------------------------------")
    cb3 = CircuitBoardProblem([(3,2),(5,2),(2,3),(7,1)],10,3)
    cb3.print_board(cb3.backtracking_search(True, True, False, True))
    print("----------")

    # # TEST 4: test CircuitBoardProblem with minimum remaining value, degree, and least constrainting value heuristics
    print("----------------------------------------------")
    print("Testing CircuitBoardProblem with mrv, degree, and lcv...")
    print("----------------------------------------------")
    cb4 = CircuitBoardProblem([(3,2),(5,2),(2,3),(7,1)],10,3)
    cb4.print_board(cb4.backtracking_search(True, True, True, True))
    print("----------")
