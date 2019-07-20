# themstates
A succinct but expressive state machine library

### Setup

    pip3 install themstates

Also available at PyPi - https://pypi.python.org/pypi/themstates
    
### Example

#### Code

```python
from themstates import StateMachine

sm = StateMachine()

# Define 'from' state -> 'event' -> 'to' state
sm.define('solid -> melt -> liquid')
sm.define('liquid -> vaporize -> gas')
sm.define('gas -> condense -> liquid')
sm.define('liquid -> freeze -> solid')

print('All states', sm.get_states()) #Lets see if we have all our 

# Generic action that we want to execute on state change
def some_action_function(event, payload):
            print(event, payload)
            
print('Actionable states', sm.get_actionable_states())
    
sm.add_action('solid', some_action_function)
sm.add_action('liquid', some_action_function)
sm.add_action('gas', some_action_function)

print('Actionable states', sm.get_actionable_states())

sm.start('liquid')

sm.handle('freeze', 'its getting cold')
print('Current State', sm.get_current_state())
sm.handle('vaporize', 'does nothing to a solid')
print('Current State', sm.get_current_state())
print('Previous state', sm.get_previous_state())
sm.handle('melt', 'its getting hot')
sm.handle('vaporize', 'cloudy now')

sm.reset()
print(sm.get_history())

```
    
