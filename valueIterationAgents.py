# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    """
      Your value iteration agent should take an mdp on
      construction, run the indicated number of iterations
      and then act according to the resulting policy.
    
      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state, action, nextState)
    """
    """
      self.states:
      ['TERMINAL_STATE', (0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)]
      startState:
      (0, 0)
      possibleActions:
      ('north', 'west', 'south', 'east')
      getTransitionStatesAndProbs:  //for start state using possibleActions[0]:
      [((0, 1), 0.8), ((1, 0), 0.1), ((0, 0), 0.1)]
      self.values: a dictionary with all the states and values
    """
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = util.Counter() # A Counter is a dict with default 0
    "*** YOUR CODE HERE ***"
    # self.states = self.mdp.getStates()
    # startState = self.mdp.getStartState()
    # possibleActions = self.mdp.getPossibleActions(startState)
    # probs = self.mdp.getTransitionStatesAndProbs(startState, possibleActions[0])
    
    # currState = startState
    # for action in possibleActions:
    #   transition = self.mdp.getTransitionStatesAndProbs(currState, action)
    #   print "transition:"
    #   print transition
    #   nextState = transition[0][0]
    #   print "nextState:"
    #   print nextState
      # prob = transition[1]
      # r = self.mdp.getReward(currState, action, nextState)

    """
    pseudo code
    Vk = .... Vk-1
    current time step is from the last one lookahead
    OH!
    SO WHEN There is only one second, it gets rewards right now (exit reward or living cost)
    when there are two seconds, then add all the nextState values computed from last time
    backwards recursive.
    now HOW DO I DO THIS RECURSIVELY???---
    ok try doing it iteratively

    now write a for loop manually first to test
    when there's only one second in the world aka 
    k = 1:
    terminal reward or living cost
    k = 2:
    s's reward + sPrime's discounted value from previous calculation
    and weighed into probs
    k = 3:
    s's reward + sPrime's value, if exist in dictionary --- actually count() solves the problem
    etc.

    """
    allStates = self.mdp.getStates()
    currentState = self.mdp.getStartState()
    #TODO: currentState is ALWAYS BETWEEN 0,0 AND 0,1
    currentStates = []
    currentStates.append(currentState)
    allActions = self.mdp.getPossibleActions(currentState)
    k = 0
    while k<self.iterations:
      k = k + 1 #number of steps available in this world. what do we do? update
      chooseAction = util.Counter()
      for currentState in currentStates:
        for action in allActions:
          transition = self.mdp.getTransitionStatesAndProbs(currentState, action)
          for each in transition:
            # expectimax for this action, with future discounted rewards etc
            nextState = each[0]
            prob = each[1]
            currentReward = self.mdp.getReward(currentState, action, nextState)
            discountedFuture = self.values[nextState]*self.discount
            result = chooseAction[action]
            result += prob*(currentReward+discountedFuture)
            chooseAction[action] = result
        bestAction = chooseAction.argMax()
        bestValue = chooseAction[bestAction]
        self.values[currentState] = bestValue
        bestTransition = self.mdp.getTransitionStatesAndProbs(currentState, bestAction)
        currentStates = [] 
        currentStates = [x[0] for x in bestTransition]
      
      print "self.values:"
      print self.values
      print "k = "
      print k

      # bestActionItem = max(chooseAction, key = lambda x: x[1])[0]
      # bestAction = bestActionItem[0]
      # bestResult = 
      # self.values[currentState] = 

  def getValue(self, state):
    """
      Return the value of the state (computed in __init__).
    """

    return self.values[state]


  def getQValue(self, state, action):
    """
      The q-value of the state action pair
      (after the indicated number of value iteration
      passes).  Note that value iteration does not
      necessarily create this quantity and you may have
      to derive it on the fly.
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    "*** YOUR CODE HERE ***"
    action = self.mdp.getPossibleActions(state)
    return action
    util.raiseNotDefined()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
