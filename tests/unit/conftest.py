"""Global fixtures."""

from __future__ import unicode_literals

from mock import Mock
import pytest


@pytest.fixture
def kms_client():
    """A mocked version of boto3 DynamoDB client."""
    mocked = Mock()
    mocked.decrypt = Mock(return_value={"Plaintext": b"dummy"})
    return mocked


@pytest.fixture
def kinesis_client():
    """A mocked version of boto3 Kinesis client."""
    mocked = Mock()
    ok_resp = {"ResponseMetadata": {"HTTPStatusCode": 200}}
    mocked.put_records = Mock(return_value=ok_resp)
    mocked.put_record_batch = Mock(return_value=ok_resp)
    return mocked


@pytest.fixture
def dynamodb_resource():
    """A mocked version of boto3 DynamoDB resource."""
    mock_item = Mock()
    mock_item.value = "encrypted"
    mock_item.get = Mock(return_value=None)
    rv = {"Item": mock_item}
    mocked_table = Mock()
    mocked_table.get_item = Mock(return_value=rv)
    mocked = Mock()
    mocked.Table = Mock(return_value=mocked_table)
    return mocked


@pytest.fixture
def dynamodb_client():
    """DynamoDB client."""
    mocked = Mock()
    rv = {"Item": {"value": {"B": "encrypted"}}}
    mocked.get_item = Mock(return_value=rv)
    mocked.decrypt = Mock(return_value={"Plaintext": b"dummy"})
    return mocked


@pytest.fixture
def boto3_client(kinesis_client, kms_client, dynamodb_client):
    """A mock for boto3.client."""
    def produce_client(name):
        return {"kinesis": kinesis_client, "kms": kms_client,
                "firehose": kinesis_client,
                "dynamodb": dynamodb_client}[name]

    mocked = Mock(side_effect=produce_client)
    return mocked


@pytest.fixture
def boto3_resource(dynamodb_resource):
    """A mock for boto3.resource."""
    def produce_resource(name):
        return {"dynamodb": dynamodb_resource}[name]

    mocked = Mock(side_effect=produce_resource)
    return mocked


@pytest.fixture(autouse=True)
def global_patch(boto3_client, boto3_resource, monkeypatch):
    """Patch boto3."""
    monkeypatch.setattr("boto3.client", boto3_client)
    monkeypatch.setattr("boto3.resource", boto3_resource)
