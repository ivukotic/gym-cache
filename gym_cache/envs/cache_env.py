import os
import time
import signal
import gym
from gym import error, spaces
from gym import utils
from gym.utils import seeding

import logging
logger = logging.getLogger(__name__)


class CacheEnv(gym.Env, utils.EzPickle):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.viewer = None
        self.server_process = None
        self.server_port = None
        self._configure_environment()
        self.observation_space = spaces.Box(low=-1, high=1,
                                            shape=(self.env.getStateSize()))
        # Action space omits the Tackle/Catch actions, which are useful on defense
        self.action_space = spaces.Tuple((spaces.Discrete(3),
                                          spaces.Box(low=0, high=100, shape=1),
                                          spaces.Box(low=-180, high=180, shape=1),
                                          spaces.Box(low=-180, high=180, shape=1),
                                          spaces.Box(low=0, high=100, shape=1),
                                          spaces.Box(low=-180, high=180, shape=1)))
        # self.status = hfo_py.IN_GAME

    def __del__(self):
        # self.env.act(hfo_py.QUIT)
        self.env.step()
        os.kill(self.server_process.pid, signal.SIGINT)
        if self.viewer is not None:
            os.kill(self.viewer.pid, signal.SIGKILL)

    def _configure_environment(self):
        """
        Provides a chance for subclasses to override this method and supply
        a different server configuration. By default, we initialize one
        offense agent against no defenders.
        """
        return

    def _start_viewer(self):
        # """
        # Starts the CacheWindow visualizer. Note the viewer may also be
        # used with a *.rcg logfile to replay a game. See details at
        # https://github.com/LARG/HFO/blob/master/doc/manual.pdf.
        # """
        # cmd = hfo_py.get_viewer_path() +\
        #     " --connect --port %d" % (self.server_port)
        # self.viewer = subprocess.Popen(cmd.split(' '), shell=False)
        return

    def _step(self, action):
        self._take_action(action)
        self.status = self.env.step()
        reward = self._get_reward()
        ob = self.env.getState()
        episode_over = False  # self.status != hfo_py.IN_GAME
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

    def _reset(self):
        # """ Repeats NO-OP action until a new episode begins. """
        # while self.status == hfo_py.IN_GAME:
        #     self.env.act(hfo_py.NOOP)
        #     self.status = self.env.step()
        # while self.status != hfo_py.IN_GAME:
        #     self.env.act(hfo_py.NOOP)
        #     self.status = self.env.step()
        return self.env.getState()

    def _render(self, mode='human', close=False):
        """ Viewer only supports human mode currently. """
        if close:
            if self.viewer is not None:
                os.kill(self.viewer.pid, signal.SIGKILL)
        else:
            if self.viewer is None:
                self._start_viewer()


ACTION_LOOKUP = {
    0: "dontCache",
    1: "Cache"
}
