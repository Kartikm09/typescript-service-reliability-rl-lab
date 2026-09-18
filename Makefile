PYTHON ?= python3
TASK ?= task-001
PATCH ?= tasks/$(TASK)/golden/solution.patch
REPORT ?= reports/evaluations/$(TASK)/manual
.PHONY: setup format lint typecheck build test integration-test coverage benchmark evaluator-test evaluate verify-evaluations security-scan verify-all http-smoke
setup:
	node --version
	npm --version
	npm ci
format:
	npm run format:check
lint:
	npm run lint
typecheck:
	npm run typecheck
build:
	npm run build
test:
	npm test
integration-test:
	npm run test:integration
http-smoke:
	npm run test:smoke
coverage:
	npm run coverage
benchmark:
	npm run benchmark
evaluator-test:
	PYTHONPATH=evaluator/src $(PYTHON) -m unittest discover -s evaluator/tests -v
evaluate:
	PYTHONPATH=evaluator/src $(PYTHON) -m rl_evaluator.cli evaluate --repo-root . --task $(TASK) --patch $(PATCH) --output $(REPORT)
verify-evaluations:
	$(PYTHON) scripts/verify_evaluations.py
security-scan:
	$(PYTHON) scripts/secret_scan.py
verify-all: format lint typecheck build test integration-test coverage evaluator-test verify-evaluations security-scan
	$(PYTHON) scripts/validate_repository.py
