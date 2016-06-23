# -*- coding: utf-8 -*-
"""Tests the input and output Kinesis streams."""

import time


def get_all_records(client, si, limit, timeout=10):
    """Retrieve all records from a Kinesis stream."""
    retrieved_recs = []
    for _ in range(timeout):
        kinesis_recs = client.get_records(ShardIterator=si, Limit=limit)
        si = kinesis_recs["NextShardIterator"]
        retrieved_recs += kinesis_recs["Records"]
        if len(retrieved_recs) == limit:
            # All records have been retrieved
            break
        time.sleep(1)

    return retrieved_recs


def test_get_notifications(
        environment, s3keys, kinesis, shard_iterators, output_stream_name):
    """Put and read a record from the input stream."""

    retrieved_recs = []
    timeout = min(max(15, 4 * len(s3keys), 150))
    for si in shard_iterators:
        retrieved_recs += get_all_records(kinesis, si, len(s3keys), timeout)

    import pdb; pdb.set_trace()
    assert len(retrieved_recs) == 2*len(s3keys)
    retrieved_names = {x["s3"]["name"] for x in retrieved_recs}
    assert not retrieved_names.difference(s3keys)
    assert all("input_filter" in ev and "input_mapper" in ev
               for ev in retrieved_recs)
