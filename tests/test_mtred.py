#!/usr/bin/env python
#
# Copyright (c) 2011 Ricardo Martins
#
# Licensed under the MIT License.
# http://www.opensource.org/licenses/mit-license.php

from nose.tools import *

from mtred import Worker, MtRed, MtRedError

EXAMPLE_DATA = [
    {"balance":"0.00000000","rsolved":"0","server":{"hashrate":150467.02093653,"workers":626,"roundshares":304965,"foundblock":0},"workers":{"my_miner":{"rsolved":"0","mhash":0}}},
    {"balance":"0.00000000","rsolved":"0","server":{"hashrate":150467.02093653,"workers":626,"roundshares":304965,"foundblock":0},"workers":{}},
    {"balance":"1.23456789","rsolved":"54","server":{"hashrate":150467.02093653,"workers":626,"roundshares":304965,"foundblock":0},"workers":{"my_miner":{"rsolved":"54","mhash":666.6}}},
    {"balance":"1.23456789","rsolved":"145","server":{"hashrate":150467.02093653,"workers":626,"roundshares":304965,"foundblock":0},"workers":{"my_miner":{"rsolved":"54","mhash":666.6},"my_miner_2":{"rsolved":"91","mhash":300.4}}}
]


INVALID_KEY = {"error":"Invalid Key"}

class TestWorker:
    pass

class TestMtRed:

    @raises(MtRedError)
    def test_invalid_key(self):
        client = MtRed(INVALID_KEY)

    def test_inactive_client(self):
        client = MtRed(EXAMPLE_DATA[0])

        assert_equal(client.balance, 0)
        assert_equal(client.solved_shares, 0)
        assert_equal(client.percent_share, 0)
        assert_equal(client.estimated_reward, 0)
        assert_equal(client.aggregate_hashrate, 0)

    def test_active_client_no_miners(self):
        client = MtRed(EXAMPLE_DATA[1])

        assert_equal(client.balance, 0)
        assert_equal(client.solved_shares, 0)
        assert_equal(client.percent_share, 0)
        assert_equal(client.estimated_reward, 0)
        assert_equal(client.aggregate_hashrate, 0)

    def test_active_client_single_miner(self):
        client = MtRed(EXAMPLE_DATA[2])

        assert_equal(client.balance, 1.23456789)
        assert_equal(client.solved_shares, 54)
        assert_equal(client.percent_share, 54 * 1.0/304965)
        assert_almost_equal(client.estimated_reward, MtRed.BLOCK_REWARD * 54*1.0/304965)
        assert_equal(client.aggregate_hashrate, 666.6)

    def test_active_client_two_miners(self):
        client = MtRed(EXAMPLE_DATA[3])

        assert_equal(client.balance, 1.23456789)
        assert_equal(client.solved_shares, 54+91)
        assert_equal(client.percent_share, (54+91) * 1.0/304965)
        assert_almost_equal(client.estimated_reward, MtRed.BLOCK_REWARD * (54+91)*1.0/304965)
        assert_equal(client.aggregate_hashrate, 666.6+300.4)
