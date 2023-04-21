from __future__ import annotations
from random import random
from dataclasses import dataclass
from typing import Dict

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
class Resource:

   def __init__(self,name: str, amount: int):
      self.name = name
      self.amount = amount

   name : str
   amount : int

   def __str__():
     return f"{self.name} {self.amount}"

@dataclass
class Job:
    
    def __init__(self, jobName: str, duration: int, precedence: list[Job] , allocatedResource: list[Resource]):
     self.jobName = jobName
     self.duration = duration
     self.precedence = precedence
     self.allocatedResource = allocatedResource

    jobName: str
    duration: int
    precedence: list[Job]
    allocatedResource: list[Resource]

    def __str__(self):
      return f"<job> {self.jobName} {self.duration} <precedence> {self.precedence} </precedence> <resource> {self.allocatedResource} </resource> </job>"

@dataclass
class RandomJobCreator:
    
    def __init__(self, jobCount: int, maxDuration: int, maxPrecedenceCount: int, maxResourceCount: int):
     self.jobList = []
     self.jobCount = jobCount
     self.maxDuration = maxDuration
     self.maxResourceCount = maxResourceCount
     self.maxPrecedenceCount = maxPrecedenceCount
    

    def Populate(self):       
     # create jobs without precedence
     for jobIdx in range(self.jobCount):
      job = Job('job' + str(jobIdx), duration=int(random() * self.maxDuration), precedence=None, allocatedResource=None)
      self.jobList.append(job)

     # # create random precedence around jobs
     # for precedence in range(self.jobCount):
     #   if(random() * self.maxPrecedenceCount):

     return self
    
    def Clear(self):
     del self.jobList

    def GetJobList(self):
     return self.jobList

    jobList : list[Job] # list of job list

    jobIdx : int 
    jobCount : int
    maxResourceCount : int
    maxPrecedenceCount : int

def main():
  randomJobCreator = RandomJobCreator(jobCount=100, maxDuration=50, maxPrecedenceCount=3, maxResourceCount=4)
  jobList = randomJobCreator.Populate().GetJobList()

  for job in jobList:
    print(job)

if __name__ == "__main__":
  main()
  