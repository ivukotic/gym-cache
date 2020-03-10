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

    def __init__(self, InputData, CacheSize):
        self.accesses_filename = InputData + '.h5'

        self.load_access_data()
        self.seed()  # probably not needed

        self.cache_hwm = .95
        self.cache_lwm = .90
        self.cache_size = CacheSize
        self.cache_kbytes = 0
        self.cache_content = []
        self.files_processed = 0

        self.old_fID = 0
        self.old_fs = 0

        self.viewer = None

        maxes = self.accesses.max()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            # first 6 are tokens, 7th is filesize, 8th is how full is cache at the moment
            low=np.array([0, 0, 0, 0, 0, 0, 0, 0]),
            high=np.array([maxes[0], maxes[1], maxes[2], maxes[3], maxes[4], maxes[5], maxes[6], 100]),
            dtype=np.int32
        )
        print('environment loaded!')
        print('cache size [kB]:', self.cache_size)

    def load_access_data(self):
        # last variable is the fileID.
        with pd.HDFStore(self.accesses_filename) as hdf:
            print("keys in file:", self.accesses_filename, ':', hdf.keys())
            self.accesses = hdf.select('data')
            print(self.accesses.head())

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        # """ checks if cache hit HWM """
        if self.cache_kbytes > (self.cache_size * self.cache_hwm):
            print('cache cleanup starting')

        row = self.accesses.iloc[self.files_processed, :]
        fID = row['fID']
        fs = row['kB']
        # print(row['1'], row['2'], row['3'], row['4'], row['5'], row['6'], row['kB'], row['fID'])

        found_in_cache = False
        if self.files_processed == 0:
            reward = 0
        else:
            found_in_cache = self.old_fID in self.cache_content
            if found_in_cache:
                reward = self.old_fs * 0.05
            else:
                reward = self.old_fs
            if (found_in_cache and action == 0) or (not found_in_cache and action == 1):
                reward = -reward

        done = False
        self.state = [row['1'], row['2'], row['3'], row['4'], row['5'], row['6'],
                      fs, self.cache_kbytes * 100 // self.cache_size]

        # actually add file to cache
        if not found_in_cache:
            self.cache_kbytes += fs
            self.cache_content.append(fID)
        self.files_processed += 1
        self.old_fs = fs
        self.old_fID = fID
        return np.array(self.state), int(reward), done, {}

    def reset(self):
        self.files_processed = 0
        self.cache_content = []
        self.cache_kbytes = 0

    def render(self, mode='human'):
        screen_width = 600
        screen_height = 400
        scale = 1

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
