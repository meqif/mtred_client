#!/usr/bin/env python
#
# Copyright (c) 2011 Ricardo Martins
#
# Licensed under the MIT License.
# http://www.opensource.org/licenses/mit-license.php

import json
import os
import sys
import urllib

BASE_URL = 'https://www.mtred.com/api/user/key/'

def retrieve_data(api_key):
    """ Retrieve data from the pool and convert it to a dict. """
    return json.load(urllib.urlopen(BASE_URL + api_key))

class Worker(object):
    """ Represents a single miner. """

    def __init__(self, name, worker_data):
        self.name = name
        self.hashrate = float(worker_data['mhash'])
        self.solved_shares = int(worker_data['rsolved'])

class MtRedError(ValueError):
    pass

class MtRed(object):
    """ The client stats from the pool. """

    BLOCK_REWARD = 50  # will change in the future

    def __init__(self, data):
        if data.has_key('error'):
            raise MtRedError, data['error']

        self.balance = float(data['balance'])
        self.solved_shares = int(data['rsolved'])
        self.total_shares = int(data['server']['roundshares'])
        self.workers = [Worker(name,w) for name,w in data['workers'].items()]

    @property
    def percent_share(self):
        """ Returns the percentage of shares solved by the owned miners for the
        current block. """
        return self.solved_shares * 1.0 / self.total_shares

    @property
    def estimated_reward(self):
        """ Returns the estimated reward for the current block. """
        return self.BLOCK_REWARD * self.percent_share

    @property
    def aggregate_hashrate(self):
        """ Returns the aggregate hashrate of the owned miners. """
        return reduce(lambda x, y: x + y.hashrate, self.workers, 0)

def main():
    if len(sys.argv) != 2:
        print "Usage: %s [API key]" % sys.argv[0]
    else:
        client = MtRed(retrieve_data(sys.argv[1]))
        print "Balance: %d BTC%s" \
              "Estimated reward: %f BTC%s" \
              "Aggregate hashrate: %.2f Mhash/s" % (
                client.balance,
                os.linesep,
                client.estimated_reward,
                os.linesep,
                client.aggregate_hashrate)

if __name__ == '__main__':
    main()
