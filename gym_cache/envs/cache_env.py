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


class CacheEnv(gym.Env):

    metadata = {'render.modes': ['human']}
    actions_num = 1  # estimated probability that a file is in cache.

    def __init__(self):
        self.accesses_filename = 'ANALY_MWT2_UCORE_ready'
        self.cache_hwm = .95
        self.cache_lwm = .90
        self.cache_size = 1024 * 1024 * 1024  # 1GB
        self.cache_bytes = 0
        self.viewer = None
        self.state = None
        self.action_space = spaces.Box(low=0.0, high=1.0, shape=[1], dtype=np.float32)
        self.observation_space = spaces.Box(low=[0,0,0,0,0,0], high=[100,100,100,100,100,100], dtype=np.int32)

    def __del__(self):
        self.env.step()

    def load_access_data(self):
        with pd.HDFStore(pq + '.h5') as hdf:
            print("keys:", hdf.keys())
            self.accesses = hdf.select('data')

    def step(self, action):
        self._take_action(action)
        self.status = self.env.step()
        reward = self._get_reward()
        ob = self.env.getState()
        episode_over = False
        return ob, reward, episode_over, {}

    def _take_action(self, action):
        # """ Converts the action space into an HFO action. """
        # action_type = ACTION_LOOKUP[action[0]]
        # if action_type == hfo_py.DASH:
        #     self.env.act(action_type, action[1], action[2])
        # elif action_type == hfo_py.TURN:
        #     self.env.act(action_type, action[3])
        # elif action_type == hfo_py.KICK:
        #     self.env.act(action_type, action[4], action[5])
        # else:
        #     print('Unrecognized action %d' % action_type)
        #     self.env.act(hfo_py.NOOP)
        return

    def _get_reward(self):
        # """ Reward is given for scoring a goal. """
        # if self.status == hfo_py.GOAL:
        #     return 1
        # else:
        return 0

    def reset(self):
        # """ Repeats NO-OP action until a new episode begins. """
        # while self.status == hfo_py.IN_GAME:
        #     self.env.act(hfo_py.NOOP)
        #     self.status = self.env.step()
        # while self.status != hfo_py.IN_GAME:
        #     self.env.act(hfo_py.NOOP)
        #     self.status = self.env.step()
        return self.env.getState()

    def render(self, mode='human', close=False):
        """ Viewer only supports human mode currently. """
        if close:
            pass
        else:
            pass
