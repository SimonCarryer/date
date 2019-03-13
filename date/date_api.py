from .date_env import DateEnv
import json

def get_date_response(last_state, action):
    done = False
    reward = 0
    if last_state is None:
        date_env = DateEnv()
    else:
        try: 
            state = json.loads(last_state)
            date_env = DateEnv(counter=state['counter'],
                            partner_attributes=state['partner_attributes'],
                            me_attributes=state['me_attributes'],
                            previous=state['previous']
                            )
        except:
            print('uh oh')
            date_env = DateEnv()
    if action is not None:
        action_idx = date_env.action_reverse_lookup[action]
        state, reward, done = date_env.step(action_idx)
    state = date_env.render()
    return state, reward, done