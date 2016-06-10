from Numberjack import *

def get_model():
      N = param['N']
      inputtable = param['inputtable']
      capacity = 1
      output = VarArray(N, N)
      matrix = Matrix(N, N)
      cost = Sum([Sum(matrix[i], inputtable[i]) for i in range(N)])

      model = Model(
            Minimize(cost),
            [Sum(row) == 1 for row in matrix.row],
            [Sum(col) <= capacity for col in matrix.col]
            )

      return capacity, output, matrix, cost, model

def solve(param):

      capacity, output, matrix, cost, model = get_model()

      solver = model.load(param['solver'])
      solver.setVerbosity(param['verbose'])
      solver.setTimeLimit(param['tcutoff'])
      solver.solve()

      if solver.is_sat():
            print(str(matrix))
      elif solver.is_unsat():
            print('Unsatisfiable')
      else:
            print('Timed out')

if __name__ == '__main__':

      default = {'solver': 'Mistral', 'verbose': 0, 'tcutoff': 30, 'inputtable': [[2,6,4],[0,9,3],[5,5,5]], 'N': 3}
      param = input(default)
      solve(param)