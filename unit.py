import gym
env = gym.make('gym_cache:Cache-v0')
env.reset()
for i in range(120):
    act = env.action_space.sample()
    print('action:', act)
    acc, rew, done, smt = env.step(act)
    print('access:', acc, 'rew:', rew)
