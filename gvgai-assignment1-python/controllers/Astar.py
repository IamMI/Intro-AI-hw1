import copy
import random
import time
class AstarAgent:
    def __init__(self, env, tick_max):
        self.env = env
        self.tick_max = tick_max
        self.tick = 0
        self.time_max = 8000
        # Your can add new attributes if needed
        
        # 寻找key和goal的位置
        for row_index, row in enumerate(self.env.grid):
            for col_index, item in enumerate(row):
                if 'goal' in item:
                    pos_goal = [col_index, row_index]
                if 'key' in item:
                    pos_key = [col_index, row_index]
                    
        self.key_pos = pos_key
        self.goal_pos = pos_goal
        
        self.path_opt = []

    
    def eval(self, env): # 主要设计启发性算法
        box_pos = []
        hole_pos = []
        avatar_pos = env.avatar_pos
        flag = 1 if 'avatar_withkey' in env.grid[avatar_pos[1]][avatar_pos[0]] else 0
        
        for row, items in enumerate(env.grid):
            for col, item in enumerate(items):                    
                if 'box' in item:
                    box_pos.append([col, row])
                if 'hole' in item:
                    hole_pos.append([col, row])
                    
        box_num = len(box_pos)
        hole_num = len(hole_pos)
        
        if not flag:
            dis = abs(avatar_pos[1]-self.key_pos[1]) + abs(avatar_pos[0]-self.key_pos[0]) + 10
        else:
            dis = abs(avatar_pos[1]-self.goal_pos[1]) + abs(avatar_pos[0]-self.goal_pos[0]) 

        # 我们采取重点突破的策略
        # 仅针对关卡三
        hole_pos = [[4,1],[5,1]]
        # 尽可能减少箱子与这两个空洞的距离
        box_hole_dis = 0
        if box_num != 0:
            for box in box_pos:
                for hole in hole_pos:
                    box_hole_dis += abs(hole[1]-box[1]) + abs(hole[0]-box[0])
        
        # # 减少avatar与其中一个box的距离
        # dis_avatar_box = abs(avatar_pos[0]-box_pos[0][0]) + abs(avatar_pos[1]-box_pos[0][1]) if box_num != 0 else 10
        # # 减少box和hole的距离
        # dis_box_hole = abs(box_pos[0][0]-hole_pos[0][0]) + abs(box_pos[0][1]-hole_pos[0][1]) if box_num != 0 else 10
        # # 减少box和hole的数量
        # num_box_hole = box_num + hole_num
        
        return dis + (box_hole_dis)*10 # + dis_avatar_box + dis_box_hole + num_box_hole*10
    
    def makenode(self, node):
        current_env = node['current_env']
        actions = node['actions']
        nodes = []
        # 我们在current_env的基础上，往四周寻找合适的action
        for action in [1,3,4,2]:
            env = copy.deepcopy(current_env)
            state, reward, isOver, info = env.step(action)
            if  info == {'message': 'Need key to open goal'} or \
                info == {'message': 'Hit wall'} or \
                info == {'message': 'Fell into hole. Game over.'} or \
                info == {'message': 'Cannot push box. Obstacle ahead.'} or \
                info == {'message': 'Box pushed onto goal.'}:
                    continue
            
            if  info == {'message': 'Picked up key'} or \
                info == {'message': 'All goals completed. You win!'}:
                nodes = [
                    {
                       'actions': actions + [action],
                        'current_env': env,
                        'eval': self.eval(env),
                        'state_ls': node['state_ls'] + [state] 
                    }
                ]
                break
            
            if state in node['state_ls']:
                continue
            # 保存
            nodes.append(
                {
                    'actions': actions + [action],
                    'current_env': env,
                    'eval': len(node['actions'])+self.eval(env),
                    'state_ls': node['state_ls'] + [state]
                }
            )
       
        return nodes
        
    def astar(self, current_node):
        # 从当前环境开始，我们每次在限定的搜索层数寻找合适的策略
        queue = [current_node]
        for time in range(self.time_max):
            if queue == []:
                return opt_node
            # 排序
            queue = sorted(queue, key=lambda x: x['eval'])
            opt_node = queue[0]
            # 判断是否完成目标
            if opt_node['current_env'].done == True: # 完成了任务
                return queue[0]

            queue.remove(opt_node)
            queue += self.makenode(opt_node)
        # 返回最优的节点
        queue = sorted(queue, key=lambda x: x['eval'])
        print('Now my best actions are ', queue[0]['actions']) # debug
        
        return queue[0]
        


    def solve(self, current_env):
        if self.path_opt == []:
            env = copy.deepcopy(current_env)
            current_node = {
                'actions': [],
                'current_env': env,
                'eval': 0+self.eval(env),
                'state_ls': [env.grid],
            }
            start_time = time.time()
            opt_node = self.astar(current_node)
            end_time = time.time()
            print('Time used: ',end_time-start_time)
            
            self.path_opt = opt_node['actions']
            
            action = self.path_opt.pop(0)
            return action
        else:
            action = self.path_opt.pop(0)
            return action
            

    def act(self, env):  
        
        action = self.solve(env)
        return action