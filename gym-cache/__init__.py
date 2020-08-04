import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

# discrete action cache
register(
    id='Cache-v0',
    entry_point='gym-cache.envs:CacheEnv',
    kwargs={
        'InputData': 'data/MWT2_processed',
        'CacheSize': 100 * 1024 * 1024 * 1024
    },
    # reward_threshold=1.0,
    max_episode_steps=20000000,
    nondeterministic=False,
)

register(
    id='Cache-large-v0',
    entry_point='gym-cache.envs:CacheEnv',
    kwargs={
        'InputData': 'data/MWT2_processed',
        'CacheSize': 100 * 1024 * 1024 * 1024
    },
    # reward_threshold=1.0,
    max_episode_steps=20000000,
    nondeterministic=True,
)

# continuous action cache
register(
    id='Cache-continuous-v0',
    entry_point='gym-cache.envs:CacheContinousEnv',
    kwargs={
        'InputData': 'data/MWT2_processed',
        'CacheSize': 100 * 1024 * 1024 * 1024
    },
    # reward_threshold=1.0,
    max_episode_steps=20000000,
    nondeterministic=True,
)
