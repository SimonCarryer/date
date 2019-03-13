import random

reward_dict = {topic: {-1: (-1, False), 0: (0, False), 1: (1, False),  -2: (-3, True)} for topic in 
     ['cars', 'sports', 'literature', 'history', 'machine learning and artificial intelligence']}
reward_dict['flirt'] = {2: (12, True), -1: (-1, False), 0: (0, False), 1:(1, False), -2: (-6, True)}
reward_dict['leave'] = {0: (-2, True)}
reward_dict['drink'] = {0: (-1, False)}

class LoveInterest:
    def __init__(self, attributes=None):
        if attributes is None:
            topics = ['cars', 'sports', 'literature', 'history', 'machine learning and artificial intelligence']
            interests = random.sample([0, 1, 1, 2, 3], 5)
            self.interests = {topic: interest for topic, interest in zip(topics, interests)}
            self.attraction = 2
            self.romance = 0
        else:
            self.interests = attributes['interests']
            self.attraction = attributes['attraction']
            self.romance = attributes['romance']
        
    def talk(self, topic, quality):
        if quality >= 4:
            return -2
        success_level = self.interests[topic] + quality
        if success_level >= 3:
            self.attraction += 1
            return random.choice([0, 1])
        if success_level <= 2:
            self.attraction -= 1
            if self.attraction <= 0:
                return -2
            else:
                return random.choice([0, -1])
        
    def flirt(self):
        if self.attraction >= 4:
            self.romance += 1
            if self.romance >=2:
                return 2
            else:
                return random.choice([0, 1])
        else:
            self.attraction -= 1
            if self.attraction <= 0:
                return -2
            else:
                return random.choice([0, -1])

    def state(self):
        return {'interests': self.interests, 'attraction': self.attraction, 'romance': self.romance}


class Me:
    def __init__(self, attributes=None):
        if attributes is None:
            self.confidence = 0
        else:
            self.confidence = attributes['confidence']
        self.max_confidence = 4
        
    def talk(self, partner, topic):
        quality = random.randint(0, 1 + self.confidence)
        response = partner.talk(topic, quality)
        self.confidence += response
        if self.confidence > self.max_confidence:
            self.confidence = self.max_confidence
        if self.confidence < 0:
            self.confidence = 0
        return response
    
    def flirt(self, partner):
        return partner.flirt()

    def drink(self):
        self.confidence += 1
        if self.confidence > self.max_confidence:
            self.confidence = self.max_confidence
        return 0

    def leave(self):
        return 0

    def state(self):
        return {'confidence': self.confidence}

class Date():
    def __init__(self, partner_attributes=None, me_attributes=None, previous=None, counter=0):
        self.actions = ['cars', 'sports', 'literature', 'history', 'machine learning and artificial intelligence', 'flirt', 'drink', 'leave']
        self.partner = LoveInterest(attributes=partner_attributes)
        self.me = Me(attributes=me_attributes)
        self.counter = counter
        if previous is None:
            self.last_action = 0
            self.last_response = 0
        else:
            self.last_action = previous['last_action']
            self.last_response = previous['last_response']

    def action(self, action_idx):
        action = self.actions[action_idx]
        if action == 'flirt':
            response = self.me.flirt(self.partner)
        elif action == 'drink':
            response = self.me.drink()
        elif action == 'leave':
            response = self.me.leave()
        else:
            response = self.me.talk(self.partner, action)
        self.last_response = response
        self.last_action = action_idx
        self.counter += 1
        return response

    def done(self):
        return self.counter > 10

    def state(self):
        return {'previous': {'last_action': self.last_action, 
                             'last_response': self.last_response}, 
                'me_attributes': self.me.state(),
                'partner_attributes': self.partner.state(),
                'counter': self.counter
                }


class DateEnv():
    def __init__(self, reward_dict=reward_dict, counter=0, partner_attributes=None, me_attributes=None, previous=None):
        self.reward_dict = reward_dict
        self.date = Date(partner_attributes=partner_attributes, me_attributes=me_attributes, previous=previous, counter=counter)
        self.n_responses = 5
        self.n_actions = len(self.date.actions)
        self.action_lookup = {i: action for i, action in enumerate(self.date.actions)}
        self.action_reverse_lookup = {action: i for i, action in enumerate(self.date.actions)}

    def sample_actions(self):
        return random.randint(0, len(self.date.actions)-1)

    def step(self, action_idx):
        response = self.date.action(action_idx)
        reward, done = self.reward_dict[self.action_lookup[action_idx]][response]
        if self.date.done():
            done = True
        return self.parse_state(), reward, done

    def parse_state(self):
        state = self.date.state()
        return state['previous']['last_action'], state['previous']['last_response'], state['me_attributes']['confidence']

    def reset(self):
        self.date = Date()
        self.counter = 0
        return self.parse_state()

    def render(self):
        return self.date.state()

