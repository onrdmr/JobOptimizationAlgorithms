from __future__ import annotations
from random import random
from dataclasses import dataclass
from typing import Dict
from random import sample
import xml.dom.minidom

import matplotlib.pyplot as plt
from matplotlib.image import imread 

import graphviz

from queue import Queue
from collections import defaultdict

@dataclass
class ResourceDict:

 def __init__(self):
  self.resourceDict = {}

 def AddResource(self, resourceName: str, value: int):
  self.resourceDict[resourceName] = value

 def GetResourceDict(self):
  return self.resourceDict

 resourceDict : dict[str, int]



@dataclass
class Starter:

  def __init__(self):
    self.jobs = []

  jobs: list[Job]

@dataclass
class Resource:

   def __init__(self, name: str, amount: int):
      self.name = name
      self.amount = amount

   name : str
   amount : int

   def __str__():
     return f"<name>{self.name}</name> <amount>{self.amount}</amount>"

# # gereksiz 
# class Visited:
#   def __init__(self, visited):
#     self.visited = visited
#   visited: bool

@dataclass
class Job():
    
    def __init__(self, name: str, duration: int, precedence: list[Job] , allocatedResource: list[Resource]): #, visited = False):
    #  super().__init__(visited=visited)
     self.name = name
     self.duration = duration
     self.precedence = precedence
     self.nextJobs = []
     self.allocatedResource = allocatedResource
     

     self.earlyStart = 0
     self.earlyFinish = 0
     self.lateStart = 0
     self.lateFinish = 0

    name: str
    duration: int
    precedence: list[Job]
    nextJobs: list[Job]
    allocatedResource: list[Resource]
    
    earlyStart: int
    earlyFinish: int

    lateStart: int
    lateFinish: int


    def __str__(self):
      return f"<job> {self.name} {self.duration} <precedence> {'None' if self.precedence is None else ''.join([str(i) for i in self.precedence])} </precedence> <resource> {self.allocatedResource} </resource> </job>"

@dataclass
class RandomJobCreator:
    
    def __init__(self, jobCount: int, maxDuration: int, maxPrecedenceCount: int, maxResourceCount: int, independentStartCount = None):
     self.jobList = []
     self.independentStartCount = maxPrecedenceCount if independentStartCount is None else independentStartCount
     self.jobCount = jobCount
     self.maxDuration = maxDuration
     self.maxResourceCount = maxResourceCount
     self.maxPrecedenceCount = maxPrecedenceCount


    # this will populate backward graph
    def Populate(self):
     # create jobs without precedence
     for jobIdx in range(self.jobCount):

      job = Job('job' + str(jobIdx), duration=int(random() * self.maxDuration), precedence=None, allocatedResource=None)
      self.jobList.append(job)

     # create independent source count
     for idx in range(self.independentStartCount):
      self.jobList[idx].precedence = None

     for idx in range(self.independentStartCount, self.jobCount):

      mod = sample(range(0, idx), 1 + int(random() * self.maxPrecedenceCount))
      self.jobList[idx].precedence = [self.jobList[i] for i in mod]
      continue

     return self

    def Clear(self):
     del self.jobList

    def GetJobList(self):
     return self.jobList

    jobList : list[Job] # list of job list

    jobIdx : int 
    jobCount : int
    independentStartCount : int
    maxResourceCount : int
    maxPrecedenceCount : int

class JobVisitedDecorator:
  def __init__(self, job: Job, level: int):
    self.job = job
    self.level = level

  job: Job
  level: int # level in bfs

class JobsHelper:

  @classmethod
  def ToXmlPretty(self,xmlString : str):
    xmlString = "<xml>" + xmlString + "</xml>"
    dom = xml.dom.minidom.parseString(xmlString)

    self.prettyXml = dom.toprettyxml(indent=' ')

    return self.prettyXml

  @classmethod
  def ForwardPass(self):
    queue = Queue()

    for job in self.initialJobs.jobs:
      queue.put(job)

    visited = defaultdict(lambda : False)

    while queue.empty() != True:
      job : Job = queue.get()

      previousEarlyFinishMax = 0
      if job.precedence != None:
        for pJob in job.precedence:
          if pJob.earlyFinish > previousEarlyFinishMax:
            previousEarlyFinishMax = pJob.earlyFinish 

      job.earlyStart = previousEarlyFinishMax
      job.earlyFinish = job.earlyStart + job.duration
      visited[job.name] = visited

      for job in job.nextJobs:
        queue.put(job)

    del queue

  @classmethod
  def PopulateForwardGraph(self, jobs: list[Job]):
    self.initialJobs = Starter() 
    for nextJob in jobs:
      if nextJob.precedence == None or nextJob.precedence == []:
        self.initialJobs.jobs.append(nextJob)
        continue 
      for job in nextJob.precedence:
        job.nextJobs.append(nextJob)
      
    return self.initialJobs

  @classmethod
  def DrawGraph(self):
    g = graphviz.Digraph(engine='dot')
    g.attr('node', shape='rectangle')
    edges= []


    bfs = Queue()      
    nodeName = "Start"
    for job in self.initialJobs.jobs:
      edges.append((nodeName , job.name))
      bfs.put(job)

    endNodes= {}

    visited = defaultdict(lambda : False)

    while bfs.empty() != True:
      baseJob: Job = bfs.get()

      for job in baseJob.nextJobs:
        if(visited[baseJob.name]):
          continue
        edges.append((baseJob.name, job.name))
        bfs.put(job)
        if(len(job.nextJobs) == 0):
          endNodes[job.name] = job
      visited[baseJob.name] = True

    for job in endNodes.values():
      edges.append((job.name, "End"))
      

    for s, t in edges:
      g.edge(s, t)
      g.node(s, label=f'''<<TABLE BORDER="O" CELLBORDER="1" CELLSPACING="0">
                              <TR><TD>Cell 1</TD><TD ROWSPAN="2">Cell 2</TD></TR>
                              <TR><TD>Cell 3</TD><TD>Cell 4</TD></TR>
                            </TABLE>>''')


    g.render('pert', format='png')
    img = imread('pert.png')
    fig, ax = plt.subplots()
    ax.imshow(img)
    plt.show()

  initialJobs: Starter
  xmlString : str



def main():
  randomJobCreator = RandomJobCreator(jobCount=100, maxDuration=50, maxPrecedenceCount=3, maxResourceCount=4)
  jobList = randomJobCreator.Populate().GetJobList()

  xmlJob = []

  for job in jobList:
    xmlJob.append(str(job))
  
  xmlString = "".join(xmlJob)
  xmlPretty = JobsHelper.ToXmlPretty(xmlString)

  file = open("jobs.xml", "w+")
  file.write(xmlPretty)

  print(xmlPretty)

  JobsHelper.PopulateForwardGraph(jobs=jobList)

  JobsHelper.ForwardPass()

  JobsHelper.DrawGraph()





  # deneme = JobsHelper.initialJobs
  # print("deneme", len(deneme.jobs))
  # print(deneme.jobs[2])


if __name__ == "__main__":
  main()
  