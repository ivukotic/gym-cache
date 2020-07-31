# gym-cache
OpenAI based Gym environments for training RL caching agent

install it:

<code>
python -m pip install --user -e .
</code>

import it like this:

<code>
import gym
gym.make('gym_cache:Cache-v0')
</code>


observation space has following variables:
* six tokens (integers)
* file size \[kB\]
* how full is the cache at that moment

There are two discrete action environments (*Cache-v0* and *Cache-large-v0*) and one discrete action environment (*Cache-continuous-v0*).


## Data extractions and preprocessing
This is a two step procedure:
* *extract raw data* _data/extract_data.py_ - change PQ, date range
* *process raw data* _data/process_data.py_ - tokenizes filenames, generates unique fileIDs, sorts by access time.

Processed data should be copied to the directory where actor runs.
It is a parque file (.pa) with one dataframe:
* index - access time (sorted)
* six tokens derived from the filename ('1', '2', '3', '4', '5', '6')
* filesize ('kB')
* unique file identifier ('fID')


## Rewards
* always negative and correspond to cost to get the file - if it was cached it will be smaller
* files are cached irrespectively from what action actor performed for the file
* cleanup
   * discrete environment - removes ones with 


# Technical implementation in XCache server
* There are additional containers in the pod. 
    * environment container
       * recieves gstream pfc, and disk info
       * recalculates new state, reward, tokenizes recieved gstream info. 
       * memorizes last state, actors actions for each file
       * triggers cleanup at lower HWM then xcache itself. Loops through memorized paths and removes ones least probably needed. 
    * redis db - used by environment container to store actor responses
    * actor container 
    