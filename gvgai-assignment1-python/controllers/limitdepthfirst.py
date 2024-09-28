import copy


class LimitedDFSAgent:
    def __init__(self, env, tick_max):
        self.env = env
        self.tick_max = tick_max
        self.tick = 0
        self.depth_max = 3
        self.depth = 0
        # Your can add new attributes if needed
        self.state_ls = []
        
        # 寻找key和goal的位置
        for row_index, row in enumerate(self.env.grid):
            for col_index, item in enumerate(row):
                if 'goal' in item:
                    pos_goal = [row_index, col_index]
                if 'key' in item:
                    pos_key = [row_index, col_index]
                    
        self.key_pos = pos_key
        self.goal_pos = pos_goal
        self.path_opt = []
        self.count = 0
        self.flag = 0
    
    def eval(self, state):
        # 寻找avatar位置
        for row, items in enumerate(state):
            for col, item in enumerate(items):
                if 'avatar_nokey' in item or 'avatar_withkey' in item:
                    avatar_pos = [row, col]
        
        if self.flag == 0:
            return abs(self.key_pos[0]-avatar_pos[0]) + abs(self.key_pos[1]-avatar_pos[1])
        else:
            return abs(self.goal_pos[0]-avatar_pos[0]) + abs(self.goal_pos[1]-avatar_pos[1])
        

    def limiteddfs(self, current_env):
        self.depth += 1
        if self.depth > self.depth_max:
            self.depth -= 1
            return [[]]
        
        actions_ls = []
        for action in [1,3,4,2]:
            env = copy.deepcopy(current_env)
            state, reward, isOver, info = env.step(action)
            
            if  info == {'message': 'Need key to open goal'} or \
                info == {'message': 'Hit wall'} or \
                info == {'message': 'Cannot push box. Obstacle ahead.'} or \
                info == {'message': 'Fell into hole. Game over.'}:
                    continue
                
            if  info == {'message': 'Picked up key'} or \
                info == {'message': 'All goals completed. You win!'}: # 节省算力
                    return [[action]]
            
            action_next = self.limiteddfs(env)
            for actions in action_next:
                actions.insert(0, action)
                actions_ls.append(actions)
        
        self.depth -= 1
        return actions_ls
          
    def solve(self, current_env):
        env = copy.deepcopy(current_env)
        if self.path_opt == []: # 并未找到最优路径
            actions_ls = self.limiteddfs(env)
            
            grade_opt = 0xffff
            action_opt = 0
            len_opt = len(actions_ls[0])
            for actions in actions_ls:
                env = copy.deepcopy(current_env)
                for action in actions:
                    state, reward, isOver, info = env.step(action)

                grade = self.eval(state)
                if grade <= grade_opt and len(actions) <= len_opt:
                    if grade == 0:
                        self.path_opt = actions
                    grade_opt = grade
                    action_opt = actions[0]
                    len_opt = len(actions)
            
            return action_opt
        else: # 已经寻找到了最优路径
            self.count += 1
            return self.path_opt[self.count]
            

    def act(self, env):
        if self.flag == 0:
            for items in env.grid:
                for item in items:
                    if 'avatar_withkey' in item:
                        self.flag = 1
                        self.path_opt = []
                        self.count = 0 
                        break
                if self.flag == 1:
                    break
                
        action = self.solve(env)
        return action