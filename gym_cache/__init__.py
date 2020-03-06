import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='Cache-v0',
    entry_point='gym_cache.envs:CacheEnv',
    kwargs={
        'InputData': 'ANALY_MWT2_UCORE_ready',
        'CacheSize': 1024 * 1024
    },
    # reward_threshold=1.0,
    max_episode_steps=200,
    nondeterministic=False,
)

register(
    id='Cache-large-v0',
    entry_point='gym_cache.envs:CacheEnv',
    kwargs={
        'InputData': 'ANALY_MWT2_UCORE_ready',
        'CacheSize': 1024 * 1024 * 1024
    },
    # reward_threshold=1.0,
    max_episode_steps=2000,
    nondeterministic=True,
)
