#! /usr/bin/env bash

env_dir="$JENKINS_HOME/virtualenv/${JOB_NAME// /_}"

#create and activate a virtualenv
virtualenv $env_dir
. $env_dir/bin/activate

#install requirements
pip install -r requirements.txt
pip install -r requirements_test.txt

mkdir ../logs

./unit_test.sh

test_pass=$?

./run_linting.sh

python_linting=$?

coverage xml
coverage -rm

e_code=$((test_pass + rubocop + python_linting))

exit $e_code
