#!/bin/bash

cd /opt/movieparties
source /opt/movieparties/.venv/bin/activate
celery -B -A worker worker --loglevel=info
deactivate
cd -
