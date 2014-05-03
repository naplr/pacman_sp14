# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

# TODO: get rid of the default value.
def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"
  from util import Stack
  from game import Directions

  state = 0
  action = 1

  s = Stack()
  visited = []
  cstate = problem.getStartState()
  s.push((cstate, []))

  while(not s.isEmpty()):
      cstate, path = s.pop()

      if (problem.isGoalState(cstate)):
          return path

      visited.append(cstate)

      for x in problem.getSuccessors(cstate):
          if(visited.count(x[state]) != 0):
              continue

          nstate = x[state]
          npath = path + [x[action]]
          s.push((nstate, npath))

  print("Path is not found")


def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  from util import Queue
  from game import Directions

  state = 0
  action = 1

  cstate = problem.getStartState()
  if (problem.isGoalState(cstate)):
          return []

  q = Queue()
  visited = []
  q.push((cstate, []))

  while(not q.isEmpty()):
      cstate, path = q.pop()
      visited.append(cstate)

      for x in problem.getSuccessors(cstate):
          npath = path + [x[action]]

          if(visited.count(x[state]) != 0):
              continue

          if (problem.isGoalState(x[state])):
              return npath

          nstate = x[state]
          visited.append(x[state])
          q.push((nstate, npath))

  print("Path is not found")

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
  "*** YOUR CODE HERE ***"
  from util import PriorityQueue
  from game import Directions

  state = 0
  action = 1

  q = PriorityQueue()
  visited = []
  cstate = problem.getStartState()
  q.push((cstate, []), 0)

  while(not q.isEmpty()):
      (cstate, path) = q.pop()

      if (problem.isGoalState(cstate)):
          return path

      if(visited.count(cstate) != 0):
          continue

      visited.append(cstate)

      for x in problem.getSuccessors(cstate):
          npath = path + [x[action]]
          ncost = problem.getCostOfActions(npath)

          if(visited.count(x[state]) != 0):
              continue

          nstate = x[state]
          q.push((nstate, npath), ncost)

  print("Path is not found")

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
  "*** YOUR CODE HERE ***"
  from util import PriorityQueue
  from game import Directions

  state = 0
  action = 1

  q = PriorityQueue()
  visited = []
  cstate = problem.getStartState()
  q.push((cstate, []), 0)

  while(not q.isEmpty()):
      cstate, path = q.pop()

      if (problem.isGoalState(cstate)):
          return path

      if(visited.count(cstate) != 0):
          continue

      visited.append(cstate)

      for x in problem.getSuccessors(cstate):
          nstate = x[state]
          npath = path + [x[action]]

          if(visited.count(x[state]) != 0):
              continue

          gcost = problem.getCostOfActions(npath)
          hcost = heuristic(x[state], problem)

          ncost = gcost + hcost

          q.push((nstate, npath), ncost)

  print("Path is not found")
  

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
