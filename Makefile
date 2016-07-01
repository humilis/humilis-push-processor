HUMILIS := .env/bin/humilis
PIP := .env/bin/pip
PYTHON := .env/bin/python
TOX := .env/bin/tox
STAGE := DEV
HUMILIS_ENV := tests/integration/humilis-push-processor

# create virtual environment
.env:
	virtualenv .env -p python3.5

# install dev dependencies, create layers directory
develop: .env
	$(PIP) install -r requirements-test.txt

# run unit tests
test: .env
	$(PIP) install tox
	$(TOX) -e unit

# run integration tests (require deployment)
testi: .env
	$(PIP) install tox
	$(TOX) -e integration

# remove .tox and .env dirs
clean:
	rm -rf .env .tox

# deploy secrets to the environment secrets vault
secrets:
	$(PYTHON) scripts/deploy-secrets.py $(HUMILIS_ENV).yaml.j2 $(STAGE)

# create CF stacks
create-cf: develop
	$(HUMILIS) create \
	  --stage $(STAGE) \
	  --output $(HUMILIS_ENV)-$(STAGE).outputs.yaml $(HUMILIS_ENV).yaml.j2

# deploy the test environment
create: create-cf secrets

# update CF stacks
update-cf: develop
	$(HUMILIS) update \
	  --stage $(STAGE) \
	  --output $(HUMILIS_ENV)-$(STAGE).outputs.yaml $(HUMILIS_ENV).yaml.j2

# update the test deployment
update: update-cf secrets

# delete the test deployment
delete: develop
	$(PYTHON) scripts/empty-bucket.py $(HUMILIS_ENV)-$(STAGE).outputs.yaml
	$(HUMILIS) delete --stage $(STAGE) $(HUMILIS_ENV).yaml.j2

# upload to Pypi
pypi: develop
	$(PYTHON) setup.py sdist upload
