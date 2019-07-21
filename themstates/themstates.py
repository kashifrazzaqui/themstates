# A simple state machine
from collections import defaultdict

class TransitionDefinition(Exception):pass
class NotCallableAction(Exception):pass

class StateMachine:
    __INIT = "__INIT"
    __RESET = "__RESET"

    def __init__(self):
        #key: current state; value set((event, target_state))
        self._transitions = defaultdict(set)
        #key: state; value set((action_functions))
        self._actions = defaultdict(set)
        self._history = [] # list: two-tuple(event, target_state)

    def start(self, start_state, payload=None):
        """ Defines and sets up start state of the state machine"""
        self._start_state = start_state
        self._transitions[self._start_state] #adds empty transition for start state
        self._history.append((StateMachine.__INIT, self._start_state))
        self._execute_actions(StateMachine.__INIT, self._start_state, payload)

    def define(self, transition):
        """Adds a transition to the state machine

        transition : string
        transition must follow grammar : <state -> event -> new_state>
        """
        source, event, target = self._parse_transition(transition.lower())
        self._transitions[source].add((event, target))

    def add_action(self, state, action_fn):
        if callable(action_fn):
            self._actions[state].add(action_fn)
        else:
            raise NotCallableAction(action_fn)

    def handle(self, event, payload):
        """
        Processes event with given payload

        Payload is passed to action callable
        Note first state is changed then actions on new current state 
        are called in no specific order
        """
        allowed_events = self._transitions[self.get_current_state()]
        for e, t in allowed_events:
            if e == event.lower():
                self._history.append((e, t))
                self._execute_actions(e, t, payload)

    def reset(self, payload=None):
        self._history.append((StateMachine.__RESET, self._start_state))
        self._execute_actions(StateMachine.__RESET, self._start_state, payload)

    def get_states(self):
        return list(self._transitions.keys())

    def get_actionable_states(self):
        return list(self._actions.keys())

    def get_previous_state(self):
        """Returns previous state (not current)"""
        if len(self._history) > 1:
            return self._history[-2][1]
        else:
            return None

    def get_current_state(self):
        return self._history[-1][1]

    def get_history(self):
        return self._history

    def _execute_actions(self, event, state, payload):
        for a in self._actions[state]:
            a(event.lower(), payload)

    def _parse_transition(self, t):
        l = [each.strip() for each in t.split("->")]
        if len(l) is not 3:
            raise TransitionDefinition(t)
        return l[0], l[1], l[2]
