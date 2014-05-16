# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
  """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """


  def getAction(self, gameState):
    """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best

    "Add more of your code here if you want to"

    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    ghostPositions = successorGameState.getGhostPositions()
    g_distances = [g for g in ghostPositions if manhattanDistance(newPos, g) <= 2]
    ghost_score = -1000 if g_distances else 0

    newFood = successorGameState.getFood().asList()
    food_distances = [manhattanDistance(newPos, f) for f in newFood]
    food_distances.sort()
    food_score = food_distances[0] if food_distances else 1
        
    return successorGameState.getScore() + ghost_score + 1.0/food_score

def scoreEvaluationFunction(currentGameState):
  """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
  return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
  """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    selectedAction = Directions.STOP
    
    isDone = gameState.isWin() or gameState.isLose()
    if (isDone):
        return Directions.STOP

    nextAgentIndex = (self.index + 1) % gameState.getNumAgents()
    legalMoves = gameState.getLegalActions(self.index)
    isMaximizer = self.index == 0
    v = float("-inf") if isMaximizer else float("inf")
    for action in legalMoves:
        successorGameState = gameState.generateSuccessor(self.index, action)
        currentValue = self.value(nextAgentIndex, successorGameState, 1) 
        select = (currentValue > v) if isMaximizer else (current < v)
        if (select):
            selectedAction = action
            v = currentValue

    return selectedAction

  def value(self, agentIndex, gameState, step):
      isDone = gameState.isWin() or gameState.isLose()
      isDepthLimit = step/gameState.getNumAgents() >= self.depth
      if (isDone or isDepthLimit):
          return self.evaluationFunction(gameState)
      if (agentIndex == 0):
          return self.maxValue(agentIndex, gameState, step+1)
      else:
          return self.minValue(agentIndex, gameState, step+1)

  def maxValue(self, agentIndex, gameState, step):
      v = float("-inf")
      nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
      legalMoves = gameState.getLegalActions(agentIndex)
      for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex, action)
          v = max(v, self.value(nextAgentIndex, successorGameState, step))
      return v

  def minValue(self, agentIndex, gameState, step):
      v = float("inf")
      nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
      legalMoves = gameState.getLegalActions(agentIndex)
      for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex, action)
          v = min(v, self.value(nextAgentIndex, successorGameState, step))
      return v

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    selectedAction = Directions.STOP
    
    isDone = gameState.isWin() or gameState.isLose()
    if (isDone):
        return Directions.STOP

    nextAgentIndex = (self.index + 1) % gameState.getNumAgents()
    legalMoves = gameState.getLegalActions(self.index)
    isMaximizer = self.index == 0
    alpha = float("-inf")
    beta = float("inf")
    v = float("-inf") if isMaximizer else float("inf")
    for action in legalMoves:
        successorGameState = gameState.generateSuccessor(self.index, action)
        currentValue = self.value(nextAgentIndex, successorGameState, 1, alpha, beta) 
        select = (currentValue > v) if isMaximizer else (current < v)
        if (select):
            selectedAction = action
            v = currentValue

        if (isMaximizer):
            if (v > beta):
                break
            alpha = max(alpha, v)
        else:
            if (v < alpha):
                break
            beta = min(beta, v)

    #print("action={0}, value={1}".format(selectedAction, v))
    return selectedAction

  def value(self, agentIndex, gameState, step, alpha, beta):
      isDone = gameState.isWin() or gameState.isLose()
      isDepthLimit = step/gameState.getNumAgents() >= self.depth
      if (isDone or isDepthLimit):
          return self.evaluationFunction(gameState)
      if (agentIndex == 0):
          return self.maxValue(agentIndex, gameState, step+1, alpha, beta)
      else:
          return self.minValue(agentIndex, gameState, step+1, alpha, beta)

  def maxValue(self, agentIndex, gameState, step, alpha, beta):
      v = float("-inf")
      prunable = (agentIndex == 0) or (agentIndex == gameState.getNumAgents() - 1)
      nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
      legalMoves = gameState.getLegalActions(agentIndex)
      for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex, action)
          v = max(v, self.value(nextAgentIndex, successorGameState, step, alpha, beta))
          if (v > beta):
              return v
          alpha = max(alpha, v)
      return v

  def minValue(self, agentIndex, gameState, step, alpha, beta):
      v = float("inf")
      prunable = (agentIndex == 0) or (agentIndex == gameState.getNumAgents() - 1)
      nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
      legalMoves = gameState.getLegalActions(agentIndex)
      for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex, action)
          v = min(v, self.value(nextAgentIndex, successorGameState, step, alpha, beta))
          if (v < alpha):
              return v
          beta = min(beta, v)
      return v

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    selectedAction = Directions.STOP
    
    isDone = gameState.isWin() or gameState.isLose()
    if (isDone):
        return Directions.STOP

    nextAgentIndex = (self.index + 1) % gameState.getNumAgents()
    legalMoves = gameState.getLegalActions(self.index)
    isMaximizer = self.index == 0
    v = float("-inf") if isMaximizer else float("inf")
    for action in legalMoves:
        successorGameState = gameState.generateSuccessor(self.index, action)
        currentValue = self.value(nextAgentIndex, successorGameState, 1) 
        select = (currentValue > v) if isMaximizer else (current < v)
        if (select):
            selectedAction = action
            v = currentValue
    return selectedAction

  def value(self, agentIndex, gameState, step):
      isDone = gameState.isWin() or gameState.isLose()
      isDepthLimit = step/gameState.getNumAgents() >= self.depth
      if (isDone or isDepthLimit):
          return self.evaluationFunction(gameState)
      if (agentIndex == 0):
          return self.maxValue(agentIndex, gameState, step+1)
      else:
          return self.expValue(agentIndex, gameState, step+1)

  def maxValue(self, agentIndex, gameState, step):
      v = float("-inf")
      nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
      legalMoves = gameState.getLegalActions(agentIndex)
      for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex, action)
          v = max(v, self.value(nextAgentIndex, successorGameState, step))
      return v

  def expValue(self, agentIndex, gameState, step):
      v = 0
      nextAgentIndex = (agentIndex + 1) % gameState.getNumAgents()
      legalMoves = gameState.getLegalActions(agentIndex)
      for action in legalMoves:
          successorGameState = gameState.generateSuccessor(agentIndex, action)
          v += self.value(nextAgentIndex, successorGameState, step)
      v = v*1.0/len(legalMoves)
      return v

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  newPos = currentGameState.getPacmanPosition()
  food = currentGameState.getFood()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

  ghostPositions = currentGameState.getGhostPositions()
  g_distances = [g for g in newGhostStates if manhattanDistance(newPos, g.getPosition()) <= 3 and g.scaredTimer < 2]
  ghost_score = -100 * len(g_distances)

  scaredGhosts = [g for g in newGhostStates if g.scaredTimer >= 4]
  scaredGhostScore = 1
  for g in scaredGhosts:
      scaredGhostScore += manhattanDistance(newPos, g.getPosition())

  capsuleScore = 0
  if (len(scaredGhosts) < 2):
      capsules = currentGameState.getCapsules()
      capsulesDist = [manhattanDistance(newPos, e) for e in capsules]
      capsulesDist.sort()
      capsuleScore = 1000.0/capsulesDist[0] if len(capsulesDist) > 0 else 0

  newFood = currentGameState.getFood().asList()
  food_distances = [manhattanDistance(newPos, f) for f in newFood]
  food_distances.sort()
  closest_food_score = food_distances[0] if food_distances else 1
  food_score = 0
  for d in food_distances:
      food_score += d
  food_score = food_score*1.0/len(food_distances) if food_distances else 1 
      
  print("{0}, {1}, {2}, {3}, {4}, {5}".format(currentGameState.getScore(), ghost_score, 1.0/scaredGhostScore, 2.0/closest_food_score, 1.0/food_score, capsuleScore))
  print(2.0/closest_food_score)
  #return currentGameState.getScore() + ghost_score + 2.0/closest_food_score + 1.0/food_score 
  return currentGameState.getScore() + ghost_score + 1.0/scaredGhostScore + 2.0/closest_food_score + 1.0/food_score + capsuleScore

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

