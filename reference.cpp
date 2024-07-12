import numpy as np
import gym
import random 
import time
from IPython.display import clear_output

env = gym.make("FrozenLake-v1")

action_space_size = env.action_space.n
state_space_size = env.observation_space.n

q_table = np.zeros((state_space_size, action_space_size))

num_episodes = 10000
max_steps_per_episode = 100

learning_rate = 0.1
discount_rate = 0.99

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.001

reward_all_episodes = []

for episode in range(num_episodes):
    state = env.reset()[0]
    done = False
    rewards_current_episode = 0

    for step in range(max_steps_per_episode):
        exploration_rate_threshold = random.uniform(0,1)
        if exploration_rate_threshold > exploration_rate:
            action = np.argmax(q_table[state,:])
        else:
            action = env.action_space.sample()
        
        result = env.step(action) 
        print(result)

        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + learning_rate * (result[1] + discount_rate * np.max(q_table[result[0], :]))

        state = result[0]
        rewards_current_episode += result[1]

        if result[2] == True:
            break
        
    exploration_rate = min_exploration_rate + (max_exploration_rate - min_exploration_rate)*np.exp(-exploration_decay_rate*episode)

    reward_all_episodes.append(rewards_current_episode)

rewards_per_1000_episodes = np.split(np.array(reward_all_episodes), num_episodes/1000)

count = 1000

print("*****Average reward per 1000 episodes*****\n")
for r in rewards_per_1000_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000

#Print updates Q-table
print("\n\n*****Q-table*****\n")
print(q_table)

# for episode in range(3):
#     state = env.reset()[0]
#     done = False
#     print("****EPISODE ", episode + 1, "****\n\n\n\n")
#     time.sleep(1)

#     for step in range(max_steps_per_episode):
#         clear_output(wait=True)
#         env.render(mode='rgb_array')
#         time.sleep(0.3)

#         action = np.argmax(q_table[state,:])
#         result = env.step(action)

#         if result[2]:
#             clear_output(wait=True)
#             env.render()
#             if result[1] == 1:
#                 print("***You reached the goal!!****")
#                 time.sleep(3)
#             else:
#                 print("***You fell through a hole!***")
#                 time.sleep(3)
#             clear_output(wait=True)
#             break

#         state = result[0]

# env.close()


