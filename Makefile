

run-script:
	@$(MAKE) local-setup && \
	cd src && \
	python main.py

local-setup:
	echo 'starting local set-up'
	pip install --upgrade pip && \
	pip install -r requirements-dev.txt && \
	pip install -r requirements.txt && \
	cd src && \
	mkdir -p output/ && \
	echo 'local set-up complete'

run-tests:
	echo 'running tests'
	cd src && \
	coverage run -m pytest -sv ./tests && \
	coverage report -m --fail-under=90
