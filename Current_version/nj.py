from Numberjack import *
from ColourCost import *


def flatten(matrix, num):

    matches = []
    for row in range(len(matrix)):
        for item in range(len(matrix[row])):
            if matrix[row][item].get_value() == 1:
                matches += [(row + num,item)]
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
        # [Sum(col) <= 20 for col in matrix.col]
    )

    return matrix, cost, model

def solve(table):
    param = {'solver': 'SCIP', 'verbose': 0, 'tcutoff': 30,
             'inputtable':table}

    matrix, cost, model = get_model(param)
    solver = model.load(param['solver'])
    #solver.setVerbosity(param['verbose'])
    #solver.setTimeLimit(param['tcutoff'])
    try:
        solver.solve()
    except:
        return 'hi'


    if solver.is_sat():
       # print("Time:", solver.getTime())
        return matrix
    elif solver.is_unsat():
        return 'Unsatisfiable'
    else:
        return 'Timed out'

def Final(tup):
    total_table = DiffTable(tup)
    N = int(len(tup[0]))
    output = flatten(solve(total_table),N)
    return output
