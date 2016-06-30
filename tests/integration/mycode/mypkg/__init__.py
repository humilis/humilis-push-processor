
import uuid


def partition_key(event):
    return event.get("client_id", str(uuid.uuid4()))


def input_filter(event, context, **kwargs):
    event["input_filter"] = True
    return True


def input_mapper(event, context, **kwargs):
    event["input_mapper"] = True


def output_filter_1(event, context, **kwargs):
    event["output_filter_1"] = True
    return True


def output_mapper_1(event, context, **kwargs):
    event["output_mapper_1"] = True


def output_mapper_2(event, context, **kwargs):
    event["output_mapper_2"] = True


def error_filter(event, context, **kwargs):
    print(event)
    event["error_filter"] = True
    return True


def error_mapper(event, context, **kwargs):
    print(event)
    event["error_mapper"] = True
