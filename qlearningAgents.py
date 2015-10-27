# qlearningAgents.py
# ------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
  """
    Q-Learning Agent

    Functions you should fill in:
      - getQValue
      - getAction
      - getValue
      - getPolicy
      - update

    Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discount (discount rate)

    Functions you should use
      - self.getLegalActions(state)
        which returns legal actions
        for a state

    iteration is the same
    q learning: update as you go (in-place)
    Bellman eq: the same, just 

    --
    recall from the Bellman equation that the Value of a state is the maximum Q-value and the Q-value is the expected sum of the reward and discounted value of the next state

    In the Q-learning update rule, the reward plus the discounted max Q-value in the observed next state
     each time the agent selects an action, and observes a reward and a new state that may depend on both the previous state and the selected action, "Q" is updated. The core of the algorithm is a simple value iteration update. It assumes the old value and makes a correction based on the new information.

  """
  def __init__(self, **args):
    "You can initialize Q-values here..."
    ReinforcementAgent.__init__(self, **args)

    "*** YOUR CODE HERE ***"
    """
    pseudo code:
    allowed function: self.getLegalActions(state)
    create a counter for (state, action), value
      the key of counter is state action pair.
    if there is nothing learned, then it's 0.0
    every time new state gets reward, ???
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
    """
    ---but we don't need to do much in init
    """
    self.qvalues = util.Counter()



  def getQValue(self, state, action):
    """
      Returns Q(state,action)
      Should return 0.0 if we never seen
      a state or (state,action) tuple
    """
    "*** YOUR CODE HERE ***"
    # print "entering getQValue"
    item = (state, action)
    return self.qvalues[item]
    util.raiseNotDefined()


  def getValue(self, state):
    """
      Returns max_action Q(state,action)
      where the max is over legal actions.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return a value of 0.0.
    """
    "*** YOUR CODE HERE ***"
    legalActions = self.getLegalActions(state)
    if len(legalActions)<= 1:
      return 0.0
    allQValues = []
    #get all q values in the state and return the max q value
    for action in legalActions:
      allQValues.append(self.getQValue(state, action))
    highest = max(allQValues)#sort the list and get the max value and return the best state-action pair
    return highest
    util.raiseNotDefined()

  def getPolicy(self, state):
    """
      Compute the best action to take in a state.  Note that if there
      are no legal actions, which is the case at the terminal state,
      you should return None.
    """
    "*** YOUR CODE HERE ***"
    legalActions = self.getLegalActions(state)
    if len(legalActions)== 1:
      return None
    #get all actions from available actions and choose the one with highest q value
    allQValues = util.Counter() #for this state only
    for action in legalActions:
      allQValues[action] = self.getQValue(state, action)
    bestAction = allQValues.argMax()
    return bestAction
    util.raiseNotDefined()

  def getAction(self, state):
    """
      Compute the action to take in the current state.  With
      probability self.epsilon, we should take a random action and
      take the best policy action otherwise.  Note that if there are
      no legal actions, which is the case at the terminal state, you
      should choose None as the action.

      HINT: You might want to use util.flipCoin(prob)
      HINT: To pick randomly from a list, use random.choice(list)
    """
    # Pick Action
    legalActions = self.getLegalActions(state)
    action = None
    "*** YOUR CODE HERE ***"
    if len(legalActions)== 1:
      return action
    self.epsilon = self.epsilon*100
    randomInt = randint(0,100)
    if randint<=self.epsilon:
      return random.choice(legalActions)
    else:
      return self.getPolicy(state)
    util.raiseNotDefined()

  def update(self, state, action, nextState, reward):
    """
      The parent class calls this to observe a
      state = action => nextState and reward transition.
      You should do your Q-Value update here

      NOTE: You should never call this function,
      it will be called on your behalf
      Instance variables you have access to
      - self.epsilon (exploration prob)
      - self.alpha (learning rate)
      - self.discount (discount rate)
    """
    "*** YOUR CODE HERE ***"
    print "current reward---:"
    print reward
    nextAction = self.getPolicy(nextState)#assuming best action
    currentItem = (state, action)
    nextItem = (nextState, nextAction)
    nextQ = self.getValue(nextState)
    currentQ = self.getQValue(state, action)
    print "nextQ:"
    print nextQ
    print "currentQ:"
    print currentQ
    sample = reward + (self.discount*nextQ)
    ans = (1-self.alpha)*currentQ+self.alpha*sample
    print "ans:"
    print ans
    self.qvalues[currentItem] = ans


    #util.raiseNotDefined()

class PacmanQAgent(QLearningAgent):
  "Exactly the same as QLearningAgent, but with different default parameters"

  def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
    """
    These default parameters can be changed from the pacman.py command line.
    For example, to change the exploration rate, try:
        python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

    alpha    - learning rate
    epsilon  - exploration rate
    gamma    - discount factor
    numTraining - number of training episodes, i.e. no learning after these many episodes
    """
    args['epsilon'] = epsilon
    args['gamma'] = gamma
    args['alpha'] = alpha
    args['numTraining'] = numTraining
    self.index = 0  # This is always Pacman
    QLearningAgent.__init__(self, **args)

  def getAction(self, state):
    """
    Simply calls the getAction method of QLearningAgent and then
    informs parent of action for Pacman.  Do not change or remove this
    method.
    """
    action = QLearningAgent.getAction(self,state)
    self.doAction(state,action)
    return action


class ApproximateQAgent(PacmanQAgent):
  """
     ApproximateQLearningAgent

     You should only have to overwrite getQValue
     and update.  All other QLearningAgent functions
     should work as is.
  """
  def __init__(self, extractor='IdentityExtractor', **args):
    self.featExtractor = util.lookup(extractor, globals())()
    PacmanQAgent.__init__(self, **args)

    # You might want to initialize weights here.
    "*** YOUR CODE HERE ***"

  def getQValue(self, state, action):
    """
      Should return Q(state,action) = w * featureVector
      where * is the dotProduct operator
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

  def update(self, state, action, nextState, reward):
    """
       Should update your weights based on transition
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

  def final(self, state):
    "Called at the end of each game."
    # call the super-class final method
    PacmanQAgent.final(self, state)

    # did we finish training?
    if self.episodesSoFar == self.numTraining:
      # you might want to print your weights here for debugging
      "*** YOUR CODE HERE ***"
      pass
