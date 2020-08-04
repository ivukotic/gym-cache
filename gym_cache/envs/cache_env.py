# import os
# import time
# import signal
# import matplotlib.pyplot as plt
import gym
from gym import spaces
# from gym import error, utils
from gym.utils import seeding
import pandas as pd
import numpy as np

import logging
logger = logging.getLogger(__name__)


class CacheEnv(gym.Env):

    metadata = {'render.modes': ['human']}
    actions_num = 1  # best guess if the file is in the cache/should be kept in cache

    def __init__(self, InputData, CacheSize):

        self.name = '100TB'
        self.actor_name = 'default'

        self.accesses_filename = InputData + '.pa'

        self.load_access_data()
        self.seed()  # probably not needed

        self.cache_value_weight = 1.0  # applies only on files already in cache

        self.cache_size = CacheSize
        self.cache_hwm = .95 * self.cache_size
        self.cache_lwm = .90 * self.cache_size
        self.cache_kbytes = 0
        # tuples of fid: [access_no, filesize, decission]
        self.cache_content = {}
        self.files_processed = 0
        self.data_processed = 0

        self.monitoring = []

        # from previous cycle
        self.weight = 0  # delivered in next cycle.
        self.found_in_cache = False
        self.fID = None
        #########

        self.viewer = None

        maxes = self.accesses.max()
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            # first 6 are tokens, 7th is filesize, 8th is how full is cache at the moment
            low=np.array([0, 0, 0, 0, 0, 0, 0, 0]),
            high=np.array([maxes[0], maxes[1], maxes[2], maxes[3],
                           maxes[4], maxes[5], maxes[6], 100]),
            dtype=np.int32
        )
        print('environment loaded!  cache size [kB]:', self.cache_size)

    def set_actor_name(self, actor):
        self.actor_name = actor

    def load_access_data(self):
        # last variable is the fileID.
        self.accesses = pd.read_parquet(self.accesses_filename)
        # self.accesses = self.accesses.head(50000)
        self.total_accesses = self.accesses.shape[0]
        print("accesses loaded:", self.total_accesses)

    def save_monitoring_data(self):
        mdata = pd.DataFrame(self.monitoring, columns=[
                             'kB', 'cache size', 'cache hit', 'reward'])
        mdata.to_parquet('results/' + self.name + '_' +
                         self.actor_name + '.pa', engine='pyarrow')

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _cache_cleanup(self):
        # create dataframe from cache info
        acc = pd.DataFrame.from_dict(self.cache_content, orient='index', columns=[
                                     'accNo', 'fs', 'action'])
        # move accesses that we want kept to much later times
        acc['accNo'] = acc['accNo'] + acc['action']*1000000
        # order files by access instance (equivalent of time)
        acc.sort_values(by='accNo', axis=0, inplace=True)
        # starting from lowest number remove from cache
        counter = 0
        while self.cache_kbytes > self.cache_lwm:
            row = acc.iloc[counter, :]
            self.cache_kbytes -= row['fs']
            del self.cache_content[row.name]
            counter += 1
        # print('cleaned', counter, 'files.')

    def step(self, action):

        # calculate reward, this is for the access delivered in previous state
        # takes into account:
        #  * weight (was remembered from previous step),
        #  * was it in cache (was remembered from previous step),
        #  * what action actor took
        reward = self.weight
        if (self.found_in_cache and action == 0) or (not self.found_in_cache and action == 1):
            reward = -reward

        if self.fID:  # check that this is not the first access
            # remember what is the action
            prevCacheContent = self.cache_content[self.fID]
            self.cache_content[self.fID] = (
                prevCacheContent[0], prevCacheContent[1], action)

            # checks if cache hit HWM
            # print('cache filled:', self.cache_kbytes)
            if self.cache_kbytes > self.cache_hwm:
                # print('cache cleanup starting on access:', self.files_processed)
                self._cache_cleanup()

        # takes next access
        row = self.accesses.iloc[self.files_processed, :]
        self.fID = row['fID']
        fs = row['kB']
        # print(row['1'], row['2'], row['3'], row['4'], row['5'], row['6'], row['kB'], row['fID'])

        self.found_in_cache = self.fID in self.cache_content
        # print('found in cache', self.found_in_cache, self.fID, self.cache_content)
        if self.found_in_cache:
            # print('cache hit - 5%')
            self.weight = fs * self.cache_value_weight
        else:
            # print('cache miss - 100%')
            self.weight = fs
            self.cache_kbytes += fs

        self.cache_content[self.fID] = (self.files_processed, fs, )

        self.monitoring.append(
            [fs, self.cache_kbytes, self.found_in_cache, int(reward)])

        self.files_processed += 1
        self.data_processed += fs

        state = [row['1'], row['2'], row['3'], row['4'], row['5'], row['6'],
                 fs, self.cache_kbytes * 100 // self.cache_size]

        if self.files_processed == self.total_accesses:
            self.save_monitoring_data()
            self.done = True
        return np.array(state), int(reward), self.done, {}

    def reset(self):
        self.files_processed = 0
        self.cache_content = {}
        self.cache_kbytes = 0
        self.monitoring = []
        self.done = False

        return self.step(0)[0]

    def render(self, mode='human'):
        # screen_width = 600
        # screen_height = 400
        # if self.viewer is None:  # creation of entities.
        #     from gym.envs.classic_control import rendering
        #     self.viewer = rendering.Viewer(screen_width, screen_height)
        #     l, r, t, b = -20 / 2, 20 / 2, 40 / 2, -40 / 2
        #     cart = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
        #     self.carttrans = rendering.Transform()
        #     cart.add_attr(self.carttrans)
        #     self.viewer.add_geom(cart)
        # return self.viewer.render(return_rgb_array=mode == 'rgb_array')
        return

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
