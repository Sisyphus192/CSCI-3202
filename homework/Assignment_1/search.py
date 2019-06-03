# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    S = util.Stack() # to store information about the graph
    visited = list() # visited game states

    # initialize
    start = (problem.getStartState(), []) # (state, list of actions to get to state)
    S.push(start)

    while not S.isEmpty():
        u, actions = S.pop()
        if problem.isGoalState(u):
            return actions
        if u not in visited:
            visited.append(u)
            for v, action, _ in problem.getSuccessors(u): # dont care about cost in dfs
                S.push((v, actions + [action]))

    # Incase no path is found return empty list
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    Q = util.Queue()
    visited = list() # use set instead of list to prevent duplicates
 
    # initialize
    start = (problem.getStartState(), []) # (state, list of actions to get to state)
    Q.push(start)

    while not Q.isEmpty():
        u, actions = Q.pop()
        if u not in visited:
            visited.append(u)
            # Found goal node, return shortest path.
            if problem.isGoalState(u):
                return actions

            for v, action, _ in problem.getSuccessors(u): # dont care about cost in bfs
                if v not in visited and v not in Q.list: # checking for v in Q.list saves expanding a few nodes
                    Q.push((v, actions + [action])) 
                    
    # Incase no path is found return empty list
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    # Dijkstra's by any other name
    P = util.PriorityQueue()
    visited = list() # use set instead of list to prevent duplicates
 
    # initialize
    start = (problem.getStartState(), [], 0) # gamestate, actions, cost
    P.push(start, 0) # push cost for priority queue

    while not P.isEmpty():
        u, actions, totalCost = P.pop()
        if u not in visited:
            visited.append(u)
            # Found goal node, return shortest path.
            if problem.isGoalState(u):
                return actions

            for v, action, cost in problem.getSuccessors(u):
                if v not in visited and v not in P.heap: # checking for v in P.heap saves expanding a few nodes
                    P.push((v, actions + [action], totalCost + cost), totalCost + cost) 
                    
    # Incase no path is found return empty list
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    """Search the node of least total cost first."""
    P = util.PriorityQueue()
    visited = list() # use set instead of list to prevent duplicates
 
    # initialize
    start = (problem.getStartState(), [], 0) # gamestate, actions, cost
    P.push(start, 0) # push cost for priority queue

    while not P.isEmpty():
        u, actions, totalCost = P.pop()
        if u not in visited:
            visited.append(u)
            # Found goal node, return shortest path.
            if problem.isGoalState(u):
                return actions

            for v, action, cost in problem.getSuccessors(u):
                if v not in visited and v not in P.heap: # checking for v in P.heap saves expanding a few nodes
                    P.push((v, actions + [action], totalCost + cost), totalCost + cost + heuristic(v, problem)) 
                    
    # Incase no path is found return empty list
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
