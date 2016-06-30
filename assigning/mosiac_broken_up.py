from Numberjack import *
from ColourCost import * 
from math import sqrt


def flatten(matrix, num):

    matches = []
    for row in range(len(matrix)):
        for item in range(len(matrix[row])):
            if matrix[row][item].get_value() == 1:
                matches += [(row + num, item)]
    return matches


def get_model(param):

    N = len(param['inputtable'])
    costmatrix = param['inputtable']
    x = len(costmatrix[0])
    # NxN Matrix of booleans
    matrix = Matrix(N, x)
    # The overall cost of the chosen cells in 'matrix' times their
    # corresponding cost in the 'inputtable'
    cost = Sum([Sum(matrix[i], costmatrix[i]) for i in range(N)])

    model = Model(
        # finding minimum cost
        Minimize(cost),
        # only one chosen value per row
        [Sum(row) == 1 for row in matrix.row],
        # only one chosen value per column
        #[Sum(col) <= 20 for col in matrix.col]
    )

    return matrix, cost, model


def solve(table):

    param = {'solver': 'SCIP', 'verbose': 0, 'tcutoff': 30,
             'inputtable': table}

    matrix, cost, model = get_model(param)

    solver = model.load(param['solver'])
    solver.setVerbosity(param['verbose'])
    solver.setTimeLimit(param['tcutoff'])
    solver.solve()

    if solver.is_sat():
        print(str(matrix))
        return matrix
        print("Time:", solver.getTime())
    elif solver.is_unsat():
        print('Unsatisfiable')
    else:
        print('Timed out')


def Final(tup):
    total_table = DiffTable(tup)
    N = int(sqrt(len(tup[0])))
    output = []
    for x in range(0, N*N, N):
        print(x, N)
        print("total_table", total_table)
        inputtable = total_table[x:x+N]
        print(inputtable)
        output += flatten(solve(inputtable), x)
        print(output)
    return output
