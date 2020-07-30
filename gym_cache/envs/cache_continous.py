import os
import time
import signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import pandas as pd
import numpy as np

import logging
logger = logging.getLogger(__name__)


class CacheContinousEnv(gym.Env):

    metadata = {'render.modes': ['human']}
    actions_num = 1  # estimated probability that a file is in cache.

    def __init__(self, InputData, CacheSize):
        self.accesses_filename = InputData + '.pa'
        self.load_access_data()
        self.cache_hwm = .95
        self.cache_lwm = .90
        self.cache_size = CacheSize
        self.cache_kbytes = 0
        self.viewer = None
        self.state = None
        self.size_of_last_file_considered = 0
        maxes = self.accesses.max()
        self.action_space = spaces.Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(
            low=np.array([0, 0, 0, 0, 0, 0, 0, 0]),
            high=np.array([maxes[0], maxes[1], maxes[2], maxes[3], maxes[4], maxes[5], maxes[6], self.cache_size]),
            dtype=np.int32
        )
        print('environment loaded!')

    def load_access_data(self):
        self.accesses= pd.read_parquet(self.accesses_filename)
        print(self.accesses.head())

    def __del__(self):
        pass
        # self.env.step()

    def step(self, action):
        self._take_action(action)
        # self.status = self.env.step()
        reward = self._get_reward()
        ob = 99  # self.env.getState()
        episode_over = False
        return ob, reward, episode_over, {}

    def _take_action(self, action):
        # """ checks if cache hit HWM """
        if self.cache_kbytes > self.cache_size * self.cache_hwm:
            # needs a cleanup
            pass
        self.cache_kbytes += self.size_of_last_file_considered
        # """ ads last file to cache """

        return

    def _get_reward(self):
        # """ Reward is given for scoring a goal. """
        # if self.status == hfo_py.GOAL:
        #     return 1
        # else:
        return 0

    def reset(self):
        return

    def render(self, mode='human', close=False):
        """ Viewer only supports human mode currently. """
        if close:
            pass
        else:
            pass
