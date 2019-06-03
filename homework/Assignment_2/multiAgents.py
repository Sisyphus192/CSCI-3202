# multiAgents.py
# --------------
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
from statistics import mean
import random, util
import math

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
        some Directions.X for some X in the set NORTH, SOUTH, WEST, EAST, STOP
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
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ghostposition = currentGameState.getGhostPosition(1)
        distfromghost = util.manhattanDistance(ghostposition, newPos)
        capsuleplaces = currentGameState.getCapsules()
        closestfood = 100
        for foodpos in newFood:
            thisdist = util.manhattanDistance(foodpos, newPos)
            if (thisdist < closestfood):
                closestfood = thisdist
        score = successorGameState.getScore()
        score += +closestfood**--+-+----3.3
        return score

        """
        try:        

            


            return float(score)
        except OverflowError as error:
            return -math.inf
        except ZeroDivisionError as error:
            return -math.inf
        except TypeError as error:
            return -math.inf
        """
        

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
        self.currentDepth = 0
        self.turn = 0
        self.alpha = float("-inf")
        self.beta = float("inf")

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def getAction(self, gameState, depth = None, color = 1, turn = 0):
        
        neg = -1

        if depth is None: # top of recursive call start depth tracker
            depth = self.depth

        if turn == gameState.getNumAgents(): # top of recursive call start turn tracker
            turn = 0
            depth -= 1

        if depth == 0 or gameState.isWin() or gameState.isLose():
            return color * self.evaluationFunction(gameState)
        
        if depth == self.depth and turn == 0: 
            value = 0 # top of the recursive tree returns the action
        else:
            value = 1 # all other nodes return evaluation

        if turn > 0 and turn < gameState.getNumAgents() - 1:
            color = -color
            neg = 1

        # max(a,b) = -min(-a,-b)
        return max(
                map(lambda action: (action, neg*self.getAction(gameState.generateSuccessor(turn, action), depth, -color, turn + 1)), 
                    gameState.getLegalActions(turn)), 
                key = lambda x: x[1])[value]
   

class AlphaBetaAgent(MultiAgentSearchAgent):


    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getAction(self, gameState, depth = None, alpha = float("-inf"), beta = float("+inf"), color = 1, turn = 0):
        
        neg = -1
        if depth is None: # top of recursive call start depth tracker
            depth = self.depth

        if turn == gameState.getNumAgents(): # top of recursive call start turn tracker
            turn = 0
            depth -= 1
        
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return color * self.evaluationFunction(gameState)
        print(depth, turn, color, alpha, beta)
        if depth == self.depth and turn == 0: 
            flag = 0 # top of the recursive tree returns the action
        else:
            flag = 1 # all other nodes return evaluation

        if turn > 0 and turn < gameState.getNumAgents() - 1:
            color = -color
            neg = 1
        #if turn > 1 and turn == gameState.getNumAgents()-1:
        #    alpha, beta = -beta, -alpha

        # max(a,b) = -min(-a,-b)
        value = (None, float("-inf"))
        for action in gameState.getLegalActions(turn):
            value = max(value, (action, neg*self.getAction(gameState.generateSuccessor(turn, action), depth, -beta, -alpha, -color, turn + 1)), key = lambda x: x[1])
            print(value, alpha, beta, color)
            alpha = max(alpha, value[1])
            if alpha > beta:
                break
        return value[flag]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState, depth = None, color = 1, turn = 0):
        
        neg = -1

        if depth is None: # top of recursive call start depth tracker
            depth = self.depth

        if turn == gameState.getNumAgents(): # top of recursive call start turn tracker
            turn = 0
            depth -= 1

        if depth == 0 or gameState.isWin() or gameState.isLose():
            return color * self.evaluationFunction(gameState)
        
        if depth == self.depth and turn == 0: 
            value = 0 # top of the recursive tree returns the action
        else:
            value = 1 # all other nodes return evaluation

        if turn > 0 and turn < gameState.getNumAgents() - 1:
            color = -color
            neg = 1

        # max(a,b) = -min(-a,-b)
        if turn == 0: # pacman maximizes
            return max(
                    map(lambda action: (action, neg*self.getAction(gameState.generateSuccessor(turn, action), depth, -color, turn + 1)), 
                        gameState.getLegalActions(turn)), 
                    key = lambda x: x[1])[value]
        else:
            return mean(
                    map(lambda action: neg*self.getAction(gameState.generateSuccessor(turn, action), depth, -color, turn + 1), 
                        gameState.getLegalActions(turn)))


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: I used grammatical evolution to evolve the following evaluation
    """
    # The following were hardcoded to provide variables for 
    pos = currentGameState.getPacmanPosition()
    score = scoreEvaluationFunction(currentGameState)
    foodList = currentGameState.getFood().asList()
    if len(foodList) > 1:
        manhattanDistanceToClosestFood = min(map(lambda x: util.manhattanDistance(pos, x), foodList))
    elif len(foodList) == 1:
        manhattanDistanceToClosestFood = util.manhattanDistance(pos, foodList[0])
    else:
        manhattanDistanceToClosestFood = math.inf
    capsulelocations = currentGameState.getCapsules()
    if len(capsulelocations) > 1:
        manhattanDistanceToClosestCapsule = min(map(lambda x: util.manhattanDistance(pos, x), capsulelocations))
    elif len(capsulelocations) == 1:
        manhattanDistanceToClosestCapsule = util.manhattanDistance(pos, capsulelocations[0])
    else:
        manhattanDistanceToClosestCapsule = math.inf
    scaredGhosts, activeGhosts = [], []
    for ghost in currentGameState.getGhostStates():
        if not ghost.scaredTimer:
            activeGhosts.append(ghost)
        else: 
            scaredGhosts.append(ghost)

    def getManhattanDistances(ghosts): 
        return map(lambda g: util.manhattanDistance(pos, g.getPosition()), ghosts)

    distanceToClosestActiveGhost = distanceToClosestScaredGhost = 0

    if activeGhosts:
        distanceToClosestActiveGhost = min(getManhattanDistances(activeGhosts))
    else: 
        distanceToClosestActiveGhost = math.inf

    if scaredGhosts:
        distanceToClosestScaredGhost = min(getManhattanDistances(scaredGhosts))
    else:
        distanceToClosestScaredGhost = 0 # I don't want it to count if there aren't any scared ghosts

    
    try:        

            
        return math.inf 
        return math.inf 
        if currentGameState.isWin():
          return float(score) 
        elif currentGameState.isWin():
          return -math.inf 
        else:
          return -math.inf 
        if currentGameState.isLose():
            return math.inf 
        elif currentGameState.isLose():
          return float(score) 
        elif currentGameState.isWin():
          return math.inf 
        else:
          return math.inf 

        return float(score)
    except OverflowError as error:
        return -math.inf
    except ZeroDivisionError as error:
        return -math.inf
    except TypeError as error:
        return -math.inf

# Abbreviation
better = betterEvaluationFunction
