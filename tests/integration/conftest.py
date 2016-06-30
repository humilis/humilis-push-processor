"""Global conftest."""
import pytest
from collections import namedtuple
import os
import time
import uuid

from boto3facade.kinesis import Kinesis
from boto3facade.s3 import S3
from humilis.environment import Environment


@pytest.fixture(scope="session")
def settings():
    """Global test settings."""
    Settings = namedtuple(
        "Settings",
        "stage environment_path bucket_layer_name streams_layer_name")
    return Settings(
        stage=os.environ.get("STAGE", "TEST"),
        environment_path="tests/integration/humilis-push-processor.yaml.j2",
        bucket_layer_name="bucket",
        streams_layer_name="streams")


@pytest.yield_fixture(scope="session")
def environment(settings):
    """The test environment: this fixtures creates it and takes care of
    removing it after tests have run."""
    env = Environment(settings.environment_path, stage=settings.stage)
    env.create(update=True)
    yield env
    if os.environ.get("DESTROY", "yes").lower() == "yes":
        env.delete()


@pytest.fixture(scope="session")
def bucket_name(settings, environment):
    """The name of the output Kinesis stream."""
    layer = [l for l in environment.layers
             if l.name == settings.bucket_layer_name][0]
    return layer.outputs.get("BucketName")


@pytest.fixture(scope="session")
def output_stream_name(settings, environment):
    """The name of the test bucket."""
    layer = [l for l in environment.layers
             if l.name == settings.streams_layer_name][0]
    return [(layer.outputs.get("OutputStream1"), 2),
            (layer.outputs.get("OutputStream2"), 1)]


@pytest.fixture(scope="session")
def input_stream_name(settings, environment):
    """The name of the output Kinesis stream."""
    layer = [l for l in environment.layers
             if l.name == settings.streams_layer_name][0]
    return layer.outputs.get("InputStream")


@pytest.fixture(scope="session")
def kinesis():
    """Boto3 kinesis client."""
    return Kinesis().client


@pytest.fixture(scope="session")
def s3():
    """Boto3 S3 resource."""
    return S3().resource


@pytest.fixture(scope="function")
def shard_iterators(kinesis, output_stream_name):
    """Get the latest shard iterator after emptying a shard."""
    sis = []
    for stream_name, nb_shards in output_stream_name:
        for shard in range(nb_shards):
            si = kinesis.get_shard_iterator(
                StreamName=stream_name,
                ShardId="shardId-{0:012d}".format(shard),
                ShardIteratorType="LATEST")["ShardIterator"]
            # At most 5 seconds to empty the shard
            for _ in range(10):
                kinesis_recs = kinesis.get_records(ShardIterator=si,
                                                   Limit=1000)
                si = kinesis_recs["NextShardIterator"]
                time.sleep(0.2)
            sis.append(si)

    return sis


@pytest.yield_fixture(scope="function")
def s3keys(bucket_name, s3, shard_iterators):
    """Put some objects in the test bucket."""

    # Need to pass the shard_iterator fixture as an argument to make sure that
    # it's loaded before this fixture: Need to read the position in the stream
    # before we send any events there.
    bucket = s3.Bucket(bucket_name)

    keys = []
    for _ in range(5):
        random_key = str(uuid.uuid4())
        bucket.put_object(Body=b"hello", Bucket=bucket_name, Key=random_key)
        keys.append(random_key)

    yield keys
    objects = [{"Key": k} for k in keys]
    bucket.delete_objects(Delete={"Objects": objects})

    # Delete the keys so that we can destroy the bucket after tests complete
