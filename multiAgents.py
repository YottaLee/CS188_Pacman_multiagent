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

        "*** YOUR CODE HERE ***"

        myFoodScore = 0
        myGhostScore = 0
        myfinalScore = 0

        """
        Get all distance for food and ghost (manhattanDistance)
        """

        foodDistances = [manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()]
        ghostDistances = [manhattanDistance(newPos, ghostPos.getPosition()) for ghostPos in newGhostStates]

        """
        Get the closest food if there is any

        Get the closest ghost
        """
        if len(foodDistances) > 0:
            myFoodScore = min(foodDistances)

        if len(currentGameState.getFood().asList()) > len(foodDistances):
            myFoodScore = 0

        myGhostScore = min(ghostDistances)

        """
        Keep away from the nearest ghost (dis <= 2)
        """
        if myGhostScore <= 2:
            return -9999

        """
        Check if the ghost is still scared
        """
        isScared = False
        for scareTime in newScaredTimes:
            if scareTime > 0:
                isScared = True

        # if isScared is True:
        #     myfinalScore = myFoodScore + myGhostScore
        # else:
        #     myfinalScore = myFoodScore

        myfinalScore = myFoodScore

        return currentGameState.getScore() - myfinalScore


        # return successorGameState.getScore()

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

        """
        find the action with the highest score.
        
        iterate all actions avalibale
        get all successor states for each action
        get the score for each action
        check if is the better action
        
        return the best action
        """

        scoreList = []

        # print("is testing")

        for action in gameState.getLegalActions(0):
            successorStates = gameState.generateSuccessor(0, action)
            actionScore = self.my_minmax(successorStates, 1, 0)
            scoreList.append((actionScore, action))


        return max(scoreList)[1]
        # util.raiseNotDefined()


    def my_minmax(self, currentState, agentNum, idepth):

        if agentNum >= currentState.getNumAgents():
            agentNum = 0
            idepth +=1

        if idepth == self.depth:
            return self.evaluationFunction(currentState)

        actionList = currentState.getLegalActions(agentNum)

        if not actionList:
            return  self.evaluationFunction(currentState)

        valueList = []
        if agentNum == 0:
            for action in actionList:
                aValue = self.my_minmax(currentState.generateSuccessor(agentNum, action), agentNum+1, idepth)
                valueList.append((aValue, action))
            return max(valueList)[0]
        else:
            for action in actionList:
                aValue = self.my_minmax(currentState.generateSuccessor(agentNum, action), agentNum+1, idepth)
                valueList.append((aValue, action))
            return min(valueList)[0]

        #
        # iterateTimes = idepth* agentNum -1
        # if iterateTimes == 0:
        #     return self.evaluationFunction(currentState)
        #
        # if currentState.isWin() or currentState.isLose:
        #     return self.evaluationFunction(currentState)
        #
        #
        #
        # agentIndex = (agentNum - iterateTimes%agentNum) %agentNum
        # successorValues = [self.my_minmax(currentState.generateSuccessor(agentIndex,currentAction), iterateTimes-1) for currentAction in currentState.getLegalActions(agentIndex)]
        # if agentIndex == 0:
        #     return max(successorValues)
        # else:
        #     return min(successorValues)

        # util.raiseNotDefined()



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        infinity = float('inf')
        currentValue = -infinity
        currentAction = None
        alpha = - infinity
        beta = infinity

        legalActions = gameState.getLegalActions(0)
        for action in legalActions:
            successorStates = gameState.generateSuccessor(0, action)
            curValue = self.my_AlphaBetaPruning(successorStates, 1, 0, alpha, beta)
            if curValue > currentValue:
                currentValue = curValue
                currentAction = action

            if currentValue > beta:
                return currentAction
            alpha = max(alpha, currentValue)
        return currentAction

        # util.raiseNotDefined()


    def my_AlphaBetaPruning(self, successorState, agentIndex, idepth, alpha, beta):

        if agentIndex >= successorState.getNumAgents():
            agentIndex = 0
            idepth += 1
        if idepth == self.depth:
            return self.evaluationFunction(successorState)
        if successorState.isWin() or successorState.isLose():
            return  self.evaluationFunction(successorState)

        if agentIndex == 0:
            currentValue = float('-inf')
            for action in successorState.getLegalActions(agentIndex):
                currentValue = max(currentValue, self.my_AlphaBetaPruning(successorState.generateSuccessor(agentIndex, action), agentIndex+1, idepth, alpha, beta))
                if currentValue > beta:
                    return currentValue
                alpha =max(alpha, currentValue)
            return currentValue
        else:
            currentValue = float('inf')
            for action in successorState.getLegalActions(agentIndex):
                currentValue = min(currentValue, self.my_AlphaBetaPruning(successorState.generateSuccessor(agentIndex, action), agentIndex+1, idepth, alpha, beta))
                if currentValue < alpha:
                    return currentValue
                beta =min(beta, currentValue)
            return currentValue


        # util.raiseNotDefined()



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


        scoreList = []

        # print("is testing")

        for action in gameState.getLegalActions(0):
            successorStates = gameState.generateSuccessor(0, action)
            actionScore = self.my_expectminimax(successorStates, 1, 0)
            scoreList.append((actionScore, action))



        bestScore = max(scoreList)
        bestIndices = [index for index in range(len(scoreList)) if scoreList[index] == bestScore]
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"



        return scoreList[chosenIndex][1]
        # util.raiseNotDefined()

    def my_expectminimax(self, successorState, agentIndex, idepth):

        if agentIndex >= successorState.getNumAgents():
            agentIndex = 0
            idepth += 1
        if idepth == self.depth:
            return self.evaluationFunction(successorState)
        if successorState.isWin() or successorState.isLose():
            return  self.evaluationFunction(successorState)

        if agentIndex == 0:
            currentValue = float('-inf')
            for action in successorState.getLegalActions(agentIndex):
                currentValue = max(currentValue, self.my_expectminimax(successorState.generateSuccessor(agentIndex, action), agentIndex+1, idepth))

            return currentValue

        else:
            currentValueList = []
            for action in successorState.getLegalActions(agentIndex):
                currentValue = self.my_expectminimax(successorState.generateSuccessor(agentIndex, action), agentIndex+1, idepth)
                currentValueList.append(currentValue)
            return sum(currentValueList)/len(successorState.getLegalActions(agentIndex))

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    fd = [manhattanDistance( pos, fp ) for fp in currentGameState.getFood().asList()]
    gs = [g for g in currentGameState.getGhostStates()]
    nfd = 0
    if len(fd) > 0:
        nfd = min(fd)

    ngd = min([ manhattanDistance(pos, g.getPosition()) if g.scaredTimer < manhattanDistance(pos, g.getPosition()) else 9999 for g in gs ])

    if ngd <= 0:
        #print 'Threat !'
        return -9999 #nerver worse than die

    myGhostScore = 0
    newGhostStates = currentGameState.getGhostStates()
    for ghostState in newGhostStates:
        if ghostState.scaredTimer > 0:
            myGhostScore += 100
        else:
            ghostdist = manhattanDistance(ghostState.getPosition(), list(currentGameState.getPacmanPosition()))
            if ghostdist <= 1:
                myGhostScore = float('-inf')
            else:
                myGhostScore += (-ghostdist)

    score = nfd
    return scoreEvaluationFunction(currentGameState) - score + myGhostScore


    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
