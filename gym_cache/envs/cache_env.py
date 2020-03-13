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

        self.cache_size = CacheSize
        self.cache_hwm = .95 * self.cache_size
        self.cache_lwm = .90 * self.cache_size
        self.cache_kbytes = 0
        self.cache_content = {}
        self.files_processed = 0

        self.weight = 0  # delivered in next cycle.
        self.found_in_cache = False  # from previous cycle

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

    def _cache_cleanup(self):
        # order files by access instance
        acc = pd.DataFrame.from_dict(self.cache_content, orient='index', columns=['accNo', 'fs']).sort_values(by='accNo', axis=0)
        # starting from lowest number remove from cache
        counter = 0
        while self.cache_kbytes > self.cache_lwm:
            row = acc.iloc[counter, :]
            self.cache_kbytes -= row['fs']
            del self.cache_content[row.name]
            counter += 1
        print('cleaned', counter, 'files.')

    def step(self, action):

        # calculate reward from old weight, was it in cache and action
        reward = self.weight
        if (self.found_in_cache and action == 0) or (not self.found_in_cache and action == 1):
            reward = -reward

        # """ checks if cache hit HWM """
        # print('cache filled:', self.cache_kbytes)
        if self.cache_kbytes > self.cache_hwm:
            print('cache cleanup starting on access:', self.files_processed)
            self._cache_cleanup()

        row = self.accesses.iloc[self.files_processed, :]
        fID = row['fID']
        fs = row['kB']
        # print(row['1'], row['2'], row['3'], row['4'], row['5'], row['6'], row['kB'], row['fID'])

        self.found_in_cache = fID in self.cache_content
        # print('found in cache', self.found_in_cache, fID, self.cache_content)
        if self.found_in_cache:
            self.weight = fs * 0.05
        else:
            self.weight = fs
            self.cache_kbytes += fs

        self.cache_content[fID] = (self.files_processed, fs)
        self.files_processed += 1

        state = [row['1'], row['2'], row['3'], row['4'], row['5'], row['6'],
                 fs, self.cache_kbytes * 100 // self.cache_size]

        return np.array(state), int(reward), False, {}

    def reset(self):
        self.files_processed = 0
        self.cache_content = {}
        self.cache_kbytes = 0
        return self.step(0)[0]

    def render(self, mode='human'):
        screen_width = 600
        screen_height = 400

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
