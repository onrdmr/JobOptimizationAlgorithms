import plotly.figure_factory as ff
from random import random


activity_schema = {"Hafriyat": 7, "Grobeton": 2, "Temel": 7, "2.Bodrum Kat": 5, "1.Bodrum Kat": 2, "Zemin Kat": 2, "1.Normal Kat": 2, "2.Normal Kat": 2, "3.Normal Kat" : 2, "4.Normal Kat": 2}


first_job_time = 5
second_job_time = 5
third_job_time = 5

# time, first job finished, second job finished, third job finished
blocks = [[0, True, False, False] for i in range(10)] # 10 tane blok olucak

resources_by_time = []

# first job resource, second job resource, third job resource
three_resource_by = [100, 100, 100]

jobs = []
time = 0

task_number = 100
for i in range (task_number):
    dependant = i
    if(random() < 0.5):
        dependant = 0
    jobs.append(int(random() * 70) , int(random() * 70), dependant)


while True:

    time+=1



jobs = []

time = [[] for i in range(10)]


last_time = [0,0,0,0] # first_time_last, second_time_last, third_time_last

while True:
    first_job = 2 # Job A
    second_job = 2 # Job B
    third_job = 2  # Job C



    for i in range(10):
        if(blocks[i][1] and first_job > 0): # first job reserved
            jobs.append(dict(Task="Job " + str(i) , Start=last_time[1], Finish=last_time[1] + first_job_time))
            print(str(i)+ " " + str(last_time[1]) + " " + str(last_time[1] + first_job_time))
            blocks[i][0] = last_time[1] + first_job_time
            first_job = first_job-1
            blocks[i][1] = False
            blocks[i][2] = True

            continue

        if(blocks[i][2] and second_job > 0): # second job reserved
            jobs.append(dict(Task="Job " + str(i), Start=last_time[2], Finish=last_time[2] + second_job_time))
            print(str(i) + " " + str(last_time[2]) + " " + str(last_time[2] + second_job_time))

            blocks[i][0] = last_time[2] + second_job_time
            second_job = second_job-1
            blocks[i][2] = False
            blocks[i][3] = True 

            continue
        if(blocks[i][3] and third_job > 0): # third job reserved
            jobs.append(dict(Task="Job " + str(i), Start=last_time[3], Finish=last_time[3] + third_job_time))
            print(str(i) + " " + str(last_time[3]) + " " + str(last_time[3] + third_job_time))
            
            blocks[i][0] = last_time[3] + third_job_time
            third_job = third_job-1
            time[i] = blocks[i][0] + third_job_time

            continue
    
    breaking = True
    for i in range(10):
        if(blocks[i][3] == False):
            breaking = False



    for i in range(10):

        if(blocks[i][1] == True and blocks[i][0] > last_time[1]):
            last_time[1] = blocks[i][0]
        if(blocks[i][2] == True and blocks[i][0] > last_time[2]):
            last_time[1] = blocks[i][0]
        if(blocks[i][3] == True and blocks[i][0] > last_time[3]):
            last_time[2] = blocks[i][0]

    # for i in range(10):
        
    #     if(blocks[i][1] == True and blocks[i][0] > last_time[1]):
            
    if breaking:
        break
    

df = [dict(Task="Job A", Start=0, Finish=5) for i in range(100)]


fig = ff.create_gantt(jobs)
fig.show()