"""Lambda function setuptools entry point."""

from setuptools import setup, find_packages

setup(
    name="humilis-push-processor-lambda",
    version="0.0.0",
    packages=find_packages(),
    include_package_data=True,
    # We often need the latest version of boto3 so we include it as a req
    install_requires=[
        "boto3",
        "raven",
        "lambdautils>=0.7.1",
        "werkzeug",
        "contextlib2"
    ],
    classifiers=[
        "Programming Language :: Python :: 2.7"],
    zip_safe=False
)
