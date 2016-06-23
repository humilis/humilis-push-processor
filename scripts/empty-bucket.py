#!/usr/bin/env python
# -*- coding: utf-8 -*-


import subprocess
import sys
import yaml


# Name of the layer that deploys the bucket
LAYER_NAME = "bucket"


def empty_bucket(humilis_outputs, stage="dev"):
    """Empties the storage bucket associated to a deployment."""

    stage = stage.lower()
    with open(humilis_outputs, "r") as f:
        outputs = yaml.load(f.read())

    bucket = outputs[LAYER_NAME]["BucketName"]
    subprocess.run(["aws", "s3", "rm", "s3://{}/".format(bucket),
                    "--recursive"], check=False, stdout=subprocess.PIPE)

if __name__ == "__main__":
    empty_bucket(*sys.argv[1:])
