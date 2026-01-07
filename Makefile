test:
	pytest --cov-report=term-missing --cov=pysieved tests/
	pgrep -lf pysieved | grep 'pytest' | awk '{print $$1}' | xargs kill

