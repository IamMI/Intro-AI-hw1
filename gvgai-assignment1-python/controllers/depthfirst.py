import copy
class DFSAgent:
    def __init__(self, env, tick_max):
        self.env = env
        self.tick_max = tick_max
        self.tick = 0

        # Your can add new attributes if needed

    def dfs(self, node):

        env = node['current_env']
        
        for action in [1,3,4,2]:
            env_copy = copy.deepcopy(env)
            state, reward, isOver, info = env_copy.step(action)
            
            # 检查无用动作
            if  info == {'message': 'Need key to open goal'} or \
                info == {'message': 'Hit wall'} or \
                info == {'message': 'Fell into hole. Game over.'} or \
                info == {'message': 'Cannot push box. Obstacle ahead.'} or \
                info == {'message': 'Box pushed onto goal.'}:
                    continue
            # 检查绕路
            if state in node['state_ls']:
                continue
            
            node['actions'].append(action)
            node['current_env'] = env_copy
            node['state_ls'].append(state)
            
            if info == {'message': 'All goals completed. You win!'}:# 假如完成了任务
                return node
            else: # 继续递归
                node_next = self.dfs(node)
                if node_next['current_env'].done == True:
                    return node_next
                else:# 这个动作及以下均找不到路径
                    continue
                
        # 该层及以下找不到路径，返回
        node['actions'].pop(-1)
        node['state_ls'].pop(-1)
        return node    
        
            

    def solve(self):
        state = self.env.reset()  # Reset environment to start a new episode
        actions = self.env.action_space
        
        init_node = {
            'actions': [],
            'current_env': copy.deepcopy(self.env),
            'state_ls' : state,
        }
        
        
        node = self.dfs(init_node)
        return node['actions']
        