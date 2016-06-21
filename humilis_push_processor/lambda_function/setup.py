"""Lambda function setuptools entry point."""

from setuptools import setup, find_packages

from .humilis_s3_processor import __version__

setup(
    name="humilis-s3-processor-lambda",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    # We often need the latest version of boto3 so we include it as a req
    install_requires=[
        "boto3",
        "raven",
        "lambdautils>=0.4.3",
        "werkzeug",
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7"],
    zip_safe=False
)
