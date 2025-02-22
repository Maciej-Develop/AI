# ghostAgents.py
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


from pacman_multiagent.game import Agent
from pacman_multiagent.game import Actions
from pacman_multiagent.game import Directions
from pacman_multiagent.util import manhattan_distance
from pacman_multiagent import util


class GhostAgent(Agent):
    def __init__(self, index=0):
        super().__init__(index)

    def get_action(self, state):
        dist = self.get_distribution(state)
        if len(dist) == 0:
            return Directions.STOP
        else:
            return util.choose_from_distribution(dist)

    def get_distribution(self, state):
        """
        Returns a Counter encoding a distribution over actions from the provided state.
        """
        util.raise_not_defined()


class RandomGhost(GhostAgent):
    """
    A ghost that chooses a legal action uniformly at random.
    """
    def get_distribution(self, state):
        dist = util.Counter()
        for a in state.getLegalActions(self.index):
            dist[a] = 1.0
        dist.normalize()
        return dist


class DirectionalGhost(GhostAgent):
    """
    A ghost that prefers to rush Pacman, or flee when scared.
    """
    def __init__(self, index, prob_attack=0.8, prob_scared_flee=0.8):
        super().__init__(index)
        self.prob_attack = prob_attack
        self.prob_scaredFlee = prob_scared_flee
    
    def get_distribution(self, state):
        # Read variables from state
        ghost_state = state.getGhostState(self.index)
        legal_actions = state.getLegalActions(self.index)
        pos = state.getGhostPosition(self.index)
        is_scared = ghost_state.scaredTimer > 0

        speed = 1
        if is_scared:
            speed = 0.5

        action_vectors = [Actions.directionToVector(a, speed) for a in legal_actions]
        new_positions = [(pos[0]+a[0], pos[1]+a[1]) for a in action_vectors]
        pacman_position = state.getPacmanPosition()

        # Select best actions given the state
        distances_to_pacman = [manhattan_distance(pos, pacman_position) for pos in new_positions]
        if is_scared:
            best_score = max(distances_to_pacman)
            best_prob = self.prob_scaredFlee
        else:
            best_score = min(distances_to_pacman)
            best_prob = self.prob_attack
        best_actions = [action for action, distance in zip(legal_actions, distances_to_pacman) if distance == best_score]

        # Construct distribution
        dist = util.Counter()
        for a in best_actions:
            dist[a] = best_prob / len(best_actions)
        for a in legal_actions:
            dist[a] += (1-best_prob) / len(legal_actions)
        dist.normalize()
        return dist
