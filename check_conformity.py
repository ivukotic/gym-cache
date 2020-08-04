from stable_baselines.common.env_checker import check_env

# env = CustomEnv(arg1, ...)
# env = gym.make('gym_cache:Cache-v0')
env = CacheEnv()

# It will check your custom environment and output additional warnings if needed
check_env(env)
