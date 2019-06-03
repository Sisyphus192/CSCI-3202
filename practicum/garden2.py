
from ortools.sat.python import cp_model

def GardenSat():
	# create the model
	model = cp_model.CpModel()

	# create the variables
	num_vals = 3
	x = model.NewIntVar(0, num_vals - 1, 'x')
	y = model.NewIntVar(0, num_vals - 1, 'y')
	z = model.NewIntVar(0, num_vals - 1, 'z')

	# create the constraints
	model.Add(x != y)
	model.Maximize(x + 2 * y + 3 * z)

	# create a solver and solve the model
	solver = cp_model.CpSolver()
	status = solver.Solve(model)

	if status == cp_model.OPTIMAL:
		print('x = {}'.format(solver.Value(x)))
		print('y = {}'.format(solver.Value(y)))
		print('z = {}'.format(solver.Value(z)))

GardenSat()