import gym
env = gym.make('gym_cache:Cache-v0')
env.reset()
total_reward = 0
for i in range(1000000):
    if not i % 1000:
        print(i, 'total reward', total_reward)
        # env.render()
    act = env.action_space.sample()
    act = 0
    # print('action:', act)
    acc, rew, done, smt = env.step(act)
    # print('access:', acc, 'rew:', rew)
    total_reward += rew

env.close()
print('total_reward:', total_reward)
