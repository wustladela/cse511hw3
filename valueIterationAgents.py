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
    self.actions = util.Counter()
    self.newValues = util.Counter()
    "*** YOUR CODE HERE ***"
  
    # allStates = self.mdp.getStates()
    # currentState = self.mdp.getStartState()
    # #TODO: currentState is ALWAYS BETWEEN 0,0 AND 0,1
    # currentStates = []
    # currentStates.append(currentState)
    # allActions = self.mdp.getPossibleActions(currentState)
    # k = 0
    # while k<self.iterations:
    #   k = k + 1 #number of steps available in this world. what do we do? update
    #   chooseAction = util.Counter()
    #   for currentState in currentStates:
    #     for action in allActions:
    #       transition = self.mdp.getTransitionStatesAndProbs(currentState, action)
    #       for each in transition:
    #         # expectimax for this action, with future discounted rewards etc
    #         nextState = each[0]
    #         prob = each[1]
    #         currentReward = self.mdp.getReward(currentState, action, nextState)
    #         discountedFuture = self.values[nextState]*self.discount
    #         result = chooseAction[action]
    #         result += prob*(currentReward+discountedFuture)
    #         chooseAction[action] = result
    #     bestAction = chooseAction.argMax()
    #     bestValue = chooseAction[bestAction]
    #     self.values[currentState] = bestValue
    #     bestTransition = self.mdp.getTransitionStatesAndProbs(currentState, bestAction)
    #     currentStates = [] 
    #     currentStates = [x[0] for x in bestTransition]
      
    #   print "self.values:"
    #   print self.values
    #   print "k = "
    #   print k
    """
    pseudo code:
    p: transition function
    r: reward
    k: # actions available to take
    for k = 1 to ...
      for each state s
        immediateReward = getReward
        discountedFuture = ...
        expectedValue: sum of all possible next states values * probs //nextState value = R+discountedFuture

        and finally, we select the action with the best result.
    
    so---new pseudo code------
    for k = 1 to ...:
      for each state s: 
        for action in allActions:
          for eachOutcome in transition:
            immediateReward = ...
            discountedFuture = ...
            nextState value = immediateReward + discountedFuture
            result = probs * nextState value
        find the best action according to chooseAction
        return that one.

        use the batch version: each vk is computed from a fixed v(k-1) not updated at all
        use 
        ---
    collect policy according to value/action later.  
    """
    allStates = self.mdp.getStates()
    k = 0
    while k<=self.iterations:
      self.values = self.newValues.copy()
      for state in allStates:
        chooseAction = util.Counter()
        allActions = self.mdp.getPossibleActions(state)
        for action in allActions:
          transition = self.mdp.getTransitionStatesAndProbs(state, action)#       for each in transition:
          for eachOutcome in transition:
            nextState = eachOutcome[0]
            prob = eachOutcome[1]
            immediateReward = self.mdp.getReward(state, action, nextState)
            discountedFuture = self.values[nextState]*self.discount
            #add the value of nextState to our bookkeeping for this state
            result = chooseAction[action] #retrieve old value or 0.
            result += prob*(immediateReward+discountedFuture)
            chooseAction[action] = result

        bestAction = chooseAction.argMax()
        bestValue = chooseAction[bestAction]
        self.newValues[state] = bestValue
        self.actions[state] = bestAction
      k = k + 1


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
    """
    pseudo code:
    q value = 
    """
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
    return self.actions[state]
    util.raiseNotDefined()

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
  
