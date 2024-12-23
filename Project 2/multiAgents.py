# multiAgents.py
# --------------
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        best_value = float('-inf')
        best_action = 0
        for action in gameState.getLegalActions():
            succ = gameState.generateSuccessor(0, action)
            value = self.value(succ, 1, 0)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action

        util.raiseNotDefined()

    def value(self, state, agentIndex, depth):
        agentIndex = agentIndex % state.getNumAgents()
        if agentIndex == 0:
            depth += 1
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        elif agentIndex == 0: 
            return self.max_value(state, depth)
        else: 
            return self.min_value(state, agentIndex, depth)

    def max_value(self, state, depth):
        v = float('-inf')
        legalActions = state.getLegalActions(0)
        for action in legalActions:
            successor = state.generateSuccessor(0, action)
            v = max(v, self.value(successor, 1, depth))
        return v

    
    def min_value(self, state, agentIndex, depth):
        v = float('inf')
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            v = min(v, self.value(successor, agentIndex+1, depth))
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
        best_value = float('-inf')
        best_action = 0
        a = float('-inf')
        b= float('inf')
        
        for action in gameState.getLegalActions():
            succ = gameState.generateSuccessor(0, action)
            value = self.value(succ, 1, 0, a, b)
            if value > best_value:
                best_value = value
                best_action = action
            a = max(a, best_value)
         
                       
        return best_action
    
        util.raiseNotDefined()
    
    def value(self, state, agentIndex, depth, a, b):
        agentIndex = agentIndex % state.getNumAgents()
        if agentIndex == 0:
            depth += 1
        
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        elif agentIndex == 0: 
            return self.max_value(state, depth, a, b)
        else: 
            return self.min_value(state, agentIndex, depth, a, b)
    
    def max_value(self, state, depth, a, b):
        v = float('-inf')
        legalActions = state.getLegalActions(0)
        for action in legalActions:
            successor = state.generateSuccessor(0, action)
            v = max(v, self.value(successor, 1, depth, a, b))
            if v>b: return v
            a = max(a, v)
         
        return v

    
    def min_value(self, state, agentIndex, depth, a, b):
        v = float('inf')
        legalActions = state.getLegalActions(agentIndex)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            v = min(v, self.value(successor, agentIndex+1, depth, a, b))
            if v<a: return v
            b = min(b, v)
       
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
        best_value = float('-inf')
        best_action = 0
        for action in gameState.getLegalActions():
            succ = gameState.generateSuccessor(0, action)
            value = self.value(succ, 1, 0)
            if value > best_value:
                best_value = value
                best_action = action
        return best_action


    def value(self, state, agentIndex, depth):
        agentIndex = agentIndex % state.getNumAgents()
        if agentIndex == 0:
            depth += 1
        if state.isWin() or state.isLose() or depth == self.depth:
            return self.evaluationFunction(state)
        elif agentIndex == 0: 
            return self.max_value(state, depth)
        else: 
            return self.exp_value(state, agentIndex, depth)

    def max_value(self, state, depth):
        v = float('-inf')
        legalActions = state.getLegalActions(0)
        for action in legalActions:
            successor = state.generateSuccessor(0, action)
            v = max(v, self.value(successor, 1, depth))
        return v

    
    def exp_value(self, state, agentIndex, depth):
        v = 0
        legalActions = state.getLegalActions(agentIndex)
        probability = 1/len(legalActions)
        for action in legalActions:
            successor = state.generateSuccessor(agentIndex, action)
            v += probability * self.value(successor, agentIndex+1, depth)
        return v
    
        util.raiseNotDefined()
    


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = 0 
    
    
    ghostPos = currentGameState.getGhostPositions()
    pacPosition = currentGameState.getPacmanPosition()
    minDistToGhost = 9999
    
    for index, pos in enumerate(ghostPos):
        distance = util.manhattanDistance(pos, pacPosition)
        if distance < minDistToGhost:
            minDistToGhost = distance
            ghostIndex = index+1
            
    
    numCapsules  = len(currentGameState.getCapsules())
    if currentGameState.getGhostState(ghostIndex).scaredTimer > 3:
        score += 1/minDistToGhost
    else:
        score += minDistToGhost
    score -= 10 * currentGameState.getNumFood() + 100 * numCapsules
    return score

    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
