# This file parses the output of the PageRank app
#
# Sam Williams 2022

import sys

actual = {}
actual
#     Actual PageRank Results
# 10 iterations:
#   1.2528717283018032
#   0.6801633626023985
#   1.26383931343652
# 25 iterations
#   1.1702457725890418
#   0.6478702616853875
#   1.1990817755777772
# 50 iterations
#   0.6444910353469683
#   1.1923172883312738
#   1.163487440985469


# Read all lines
lines = None
with open(sys.argv[1]) as file:
    lines = [line.rstrip() for line in file]

# Remove comments and newlines
parsed = list(filter(lambda line: len(line) > 0 and line[0] != "#", lines))
line_num = 0

# Store and parse data
iterations = (10, 25,50)
probabilities = (0.001, 0.01, 0.1)
num_trials = 50
num_pages = 3


actual = {}
for i in iterations:
    actual[i] = []
    for _ in range(num_pages):
        actual[i].append(0)

#     Actual PageRank Results
# 10 iterations:
actual[10][0] = 1.2528717283018032
actual[10][1] = 0.6801633626023985
actual[10][2] = 1.26383931343652
# 25 iterations
actual[25][0] = 1.1702457725890418
actual[25][1] = 0.6478702616853875
actual[25][2] = 1.1990817755777772
# 50 iterations
actual[50][0] = 0.6444910353469683
actual[50][1] = 1.1923172883312738
actual[50][2] = 1.163487440985469


pri = {}
for i in iterations:
    pri[i] = {}
    for p in probabilities:
        pri[i][p] = []
        for _ in range(num_pages):
            pri[i][p].append([])
        for _ in range(num_trials):
            for j in range(num_pages):
                pri[i][p][j].append(float(parsed[line_num]))
                line_num = line_num + 1

# Example: for PageRank with 10 iterations, 0.01 probability, page A (0), trial 26
# print(str(pri[10][0.01][0][25]))

# 1. Calculate Relative error (|average - actual| / average)
averages = {}
for i in iterations:
    averages[i] = {}
    for p in probabilities:
        averages[i][p] = []
        for j in range(num_pages):
            averages[i][p].append(0)
            for t in range(num_trials):
                averages[i][p][j] = averages[i][p][j] + pri[i][p][j][t]

            averages[i][p][j] = averages[i][p][j] / num_trials

# Example: the average of 10 PR iterations, 0.001 probability, page B (1)
# print(str(averages[10][0.001][1]))

# Find average relative errors (RE) and average deviations (AD)
for i in iterations:
    print("--- PR "+ str(i) +" Iterations ---")
    for p in probabilities:
        re = 0
        ad = 0
        for j in range(num_pages):
            re = re + abs(actual[i][j] - averages[i][p][j]) / averages[i][p][j]
            pad = 0
            for t in range(num_trials):
                pad = pad + abs(actual[i][j] - pri[i][p][j][t])
            ad = ad + (pad / num_trials)
        re = re / num_pages
        ad = ad / num_pages
        print("RE for p="+ str(p)+": "+ str(re))
        print("AD for p="+ str(p)+": "+ str(ad))

