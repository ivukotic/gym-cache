# this actor does always the same action or a random one.

import gym

env = gym.make('gym-cache:Cache-v0')
env.reset()

total_reward = 0
for i in range(1000000):
    if not i % 1000:
        print(i, 'total reward', total_reward)
        # env.render()

    # --- random prediction
    # act = env.action_space.sample()
    # --- always predict cache miss
    act = 0

    acc, rew, done, smt = env.step(act)
    # print('access:', acc, 'rew:', rew)
    total_reward += rew

env.close()
print('Finished. Total reward:', total_reward)
