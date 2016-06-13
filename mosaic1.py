from Numberjack import *
from ColourCost import *

def flatten(matrix):

      matches = []
      for row in range(len(matrix)):
            for item in range(len(matrix[row])):
                  if matrix[row][item].get_value() == 1:
                        matches += [(row, item)]
      return matches
                        

def get_model():
      N = len(param['inputtable'])
      inputtable = param['inputtable']
      #output = VarArray(N, N)
      matrix = Matrix(N, N) #NxN Matrix of booleans
      
      #The overall cost of the chosen cells in 'matrix' times their corresponding cost in the 'inputtable'
      cost = Sum([Sum(matrix[i], inputtable[i]) for i in range(N)]) 

      model = Model(
            Minimize(cost), #finding minimum cost
            [Sum(row) == 1 for row in matrix.row], #only one chosen value per row
            [Sum(col) <= 1 for col in matrix.col] #only one chosen value per column
            )

      return matrix, cost, model

def solve(param):

      matrix, cost, model = get_model()

      solver = model.load(param['solver'])
      solver.setVerbosity(param['verbose'])
      solver.setTimeLimit(param['tcutoff'])
      solver.solve()

      if solver.is_sat():
            print(str(matrix))
            print(flatten(matrix))
            print("Time:", solver.getTime())
      elif solver.is_unsat():
            print('Unsatisfiable')
      else:
            print('Timed out')

if __name__ == '__main__':

      default = {'solver': 'Mistral', 'verbose': 0, 'tcutoff': 30, 'inputtable': DiffTable('RGBValues.txt')}
      param = input(default)
      solve(param)
