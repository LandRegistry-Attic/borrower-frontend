export PYTHONPATH=.

pip install -r requirements.txt

py.test --junitxml=TEST-INT-flask-app-medium.xml --verbose --cov-report term-missing --cov application integration_tests
