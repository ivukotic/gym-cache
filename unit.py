import gym
env = gym.make('gym_cache:Cache-v0')
env.reset()
total_reward = 0
for i in range(100000):
    if not i % 100:
        print(i, 'total reward', total_reward)
    act = env.action_space.sample()
    # print('action:', act)
    acc, rew, done, smt = env.step(act)
    # print('access:', acc, 'rew:', rew)
    total_reward += rew
