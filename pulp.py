from pulp import LpProblem, LpMinimize, LpVariable, LpStatus, lpSum, value

# Define tasks
tasks = ['Task1', 'Task2', 'Task3', 'Task4']

# Define duration of tasks
duration = {'Task1': 2, 'Task2': 3, 'Task3': 4, 'Task4': 3}

# Define resource usage of tasks
resource_usage = {'Task1': 5, 'Task2': 4, 'Task3': 3, 'Task4': 6}

# Define total available resources
total_resources = 15

# Create PuLP problem
problem = LpProblem("Resource Leveling Problem", LpMinimize)

# Create decision variables
start_times = LpVariable.dicts("Start_Time", tasks, lowBound=0, cat='Integer')

# Set objective function
problem += lpSum([start_times[task] for task in tasks]), "Minimize Total Duration"

# Add constraints for resource leveling
for task in tasks:
    problem += start_times[task] + duration[task] <= total_resources

# Add constraints for task dependencies
problem += start_times['Task1'] <= start_times['Task2']
problem += start_times['Task1'] <= start_times['Task3']
problem += start_times['Task2'] <= start_times['Task4']

# Solve the problem
problem.solve()

# Print the results
print("Status: ", LpStatus[problem.status])
for task in tasks:
    print("Task:", task, "Start Time:", value(start_times[task]))