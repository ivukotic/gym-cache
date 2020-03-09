# gym-cache
OpenAI based Gym environments for training RL caching agent

install it:

<code>
python -m pip install --user -e .
</code>

then import it like this:

<code>
import gym
gym.make('gym_cache:Cache-v0')
</code>

There are two discrete action environments (*Cache-v0* and *Cache-large-v0*) and one discrete action environment (*Cache-continuous-v0*).


observation space has following variables:
* six tokens (integers)
* size \[kB\]
* how full is the cache at that moment


