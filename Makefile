LOCAL_VENV_NAME=.venv
PYTHON=python3
STAGE?=dev
STACKS?=NetworkStack


.PHONY: all test lint synth diff deploy

local-venv:
	$(PYTHON) -m venv .venv

install-dependencies:
	pip install -r requirements.txt

lint:
	flake8 $(shell git ls-files '*.py')

test:
	pytest

synth:
	@cdk synth -c stage=$(STAGE) --output=cdk.out/$(STAGE) $(STACKS)

deploy: synth
	@cdk deploy --app=cdk.out/$(STAGE) $(STACKS)

diff:
	@cdk diff -c stage=$(STAGE) $(STACKS)

destroy:
	@cdk destroy -c stage=$(STAGE) $(STACKS)

bootstrapp-cdk-toolkit:
	@cdk bootstrap aws://$(shell cat sls_fake_ecommerce/config/$(STAGE).yaml | yq -r '.awsAccount')/$(shell cat config/$(STAGE).yaml | yq -r '.awsRegion') -c stage=$(STAGE)