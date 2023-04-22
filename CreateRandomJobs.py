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

@dataclass
class Job:
    
    def __init__(self, name: str, duration: int, precedence: list[Job] , allocatedResource: list[Resource]):
     self.name = name
     self.duration = duration
     self.precedence = precedence
     self.nextJobs = []
     self.allocatedResource = allocatedResource

    name: str
    duration: int
    precedence: list[Job]
    nextJobs: list[Job]
    allocatedResource: list[Resource]

    def __str__(self):
      return f"<job> {self.name} {self.duration} <precedence> {self.precedence} </precedence> <resource> {self.allocatedResource} </resource> </job>"

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
      mod = sample(range(0, idx), int(random() * self.maxPrecedenceCount))
      
      self.jobList[idx].precedence = [self.jobList[i] for i in mod]

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

class JobsHelper:
  @classmethod
  def ToXmlPretty(self,xmlString : str):
    xmlString = "<xml>" + xmlString + "</xml>"
    dom = xml.dom.minidom.parseString(xmlString)

    self.prettyXml = dom.toprettyxml(indent=' ')
  
    return self.prettyXml
  
  @classmethod
  def PopulateForwardGraph(self, jobs: list[Job]):
    self.initialJobs = Starter() 
    for nextJob in jobs:
      if nextJob.precedence == None:
        self.initialJobs.jobs.append(nextJob)
        continue 
      for job in nextJob.precedence:
        job.nextJobs.append(nextJob)
    return self.initialJobs

  @classmethod
  def drawGraph(self):
    g = graphviz.Digraph(engine='dot')
    g.attr('node', shape='rectangle')
    edges= []


    bfs = Queue()      
    nodeName = "Start"
    for job in self.initialJobs.jobs:
      edges.append((nodeName , job.name))
      bfs.put(job)
    
    endNodes= []

    while bfs.empty() != True:
      baseJob : Job = bfs.get()
      
      for job in baseJob.nextJobs:
        edges.append((baseJob.name, job.name))
        bfs.put(job)
        if(len(job.nextJobs) == 0):
          endNodes.append(job)

    for job in endNodes:
      edges.append((job.name, "End"))


    for s, t in edges:
      g.edge(s, t)

    g.render('pert', format='png')

    img = imread('pert.png')

    fig, ax = plt.subplots()
    ax.imshow(img)
    
    plt.show()





    edges
    print("not Implemented")

  # @classmethod
  # def drawGraph(self, jobs: list[Job]):
  #   g = graphviz.Digraph(engine='dot')
  #   g.attr('node', shape='rectangle')
  #   edges= []
  #   for job in jobs:
  #     if job.precedence == None:
  #       edges.append('Start', job.name)
      
  #     for nextJob in job.nextJobs:
  #       edges.append((job.name, nextJob.name))
  
  #   for s, t in edges:
  #     g.add(s, t)

  #   g.render('pert', format='png')

  #   img = imread('pert.png')

  #   fig, ax = plt.subplots()
  #   ax.imshow(img)
    
  #   plt.show()

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

  JobsHelper.drawGraph()

  # deneme = JobsHelper.initialJobs
  # print("deneme", len(deneme.jobs))
  # print(deneme.jobs[2])


if __name__ == "__main__":
  main()
  