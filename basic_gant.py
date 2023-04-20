from pulp import *

# Define the problem
prob = LpProblem("Minimum Time Scheduling Problem", LpMinimize)

# Define the job durations and costs
durations = {1: 2, 2: 3, 3: 1, 4: 1, 5: 1, 6: 1}
costs = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 1}

# Define the resources
resources = ['resourceA', 'resourceB', 'resourceC']

# Define the job-resource assignments
assignments = {
    1: 'resourceA',
    2: 'resourceA',
    3: 'resourceB',
    4: 'resourceC',
    5: 'resourceA',
    6: 'resourceB'
}

# Define the job dependencies
dependencies = {
    2: [1],
    3: [2],
    4: [3],
    6: [5]
}

# Define the start times of each job
start_times = LpVariable.dicts("StartTimes", durations.keys(), lowBound=0, cat='Integer')

# Define the objective function
prob += lpSum([start_times[j] + durations[j] for j in durations])

# Define the constraints
for j in durations:
    for k in dependencies.get(j, []):
        prob += start_times[j] >= start_times[k] + durations[k]
    prob += lpSum([start_times[j] + durations[j] for j in durations if assignments[j] == r]) <= 1 for r in resources
    prob += start_times[j] + durations[j] <= lpSum([start_times[k] for k in durations if k != j]) + 100 * (1 - lpSum([dependencies.get(j, [])]))
    
# Solve the problem
prob.solve()

# Print the solution
print("Minimum time:", value(prob.objective))
for j in durations:
    print("Job", j, "starts at time", value(start_times[j]))
