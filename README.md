# Constraint Satisfaction Problem

### Description

A general-purpose constraint solving algorithm that can be applied to solve different Constraint Satisfaction Problems (CSPs). A CSP has n variables (X1,...,Xn) and the goal is to assign each variable a domain Di (ex. D1 : X1 ∈ v1, v2, v3) of possible values. There are m constraints (C1,...,Cn), each specifying allowable combinations of values for some set of variables. An assignment of values to variables is the state of the problem. We want to find a complete assignment where all variables are assigned a that is consistent with the given constraints.

### Classes

**ConstraintSatisfactionProblem**

This class contains a backtracking algorithm to solve CSPs and utilizes a recursively called helper function. This function checks if the assigment is complete by checking its length. Then, it selects an unassigned variable and loops through all possible domain values. For each value, it checks if assigning it to the current variable would result in a consistent assignment. If so, it updates the assignment accordingly and makes a recursive call with this new assignment. Recursive calls are made until an assignment becomes inconsistent, at which point the algorithm backtracks, or until a solution is found. 

Various heuristics can be utilized to improve the effectiveness of the backtracking algorithm. All can be turned on and off by the booleans passed as parameters into the function that contains the backtracking algorith. 

*Minimum Remaining Values (MRV) Heuristic*

Rather than randomly selecting an unassigned variable in the backtracking algorithm, the MRV heuristic chooses the variable with the fewest legal values. heursitic can be used utilized to improve is containted within this class as it is generalized for both CircuitBoard and MapProblem. It is called by passing in a boolean when creating a ConstraintSatisfactionProblem, which is ultimatly passed to the select_unassigned_variable function in recursive backtracking. If the boolean is True, select_unassigned variable will use mrv to choose a variable rather than just selecting the first unassigned variable it finds. In the mrv function, I loop over all variables and find the one with fewest domain value options left and return it. There are sometimes ties, however, and that is where the degree heuristic comes in. It is implemented as follows and breaks such ties.

*Degree Heuristic*

The degree heuristic further improves the MRV heuristic by acting as a tie-breaker among MRV variables. Examining the variables tied for fewest legal values, it chooses the variable with the most constraints on remaining variables.

*AC-3*

AC-3 is also implemented in this class, an inference technique that checks the arc consistency of binary constraints. A specialized function tailored to each particular CSP is needed here.

**MapProblem**

The map-coloring problem selects a color for each territory in Australia. This problem involves several binary constraints–each pair of adjacent territories may not have the same color. 

**CircuitBoardProblem**

For the circuit-board layout problem, you are given a rectangular circuit board of size n x m, and k rectangular components of arbitrary sizes. The goal is to lay the components out in such a way that they do not overlap. For example, perhaps you are given these components and are asked to lay them out on a 10x3 grid:

```
      bbbbb   cc
aaa   bbbbb   cc  eeeeeee
aaa           cc
```

A solution might be:

```
eeeeeee.cc
aaabbbbbcc
aaabbbbbcc
```

### Testing

To run tests on the MapProblem, enter ```python3 MapProblem.py``` in the command line.

To run tests on the CircuitBoardProblem, enter ```python3 CircuitBoardProblem.py``` in the command line.
