#!/bin/bash

set -eo pipefail

if [ -z $VIRTUAL_ENV ]; then
  source venv/bin/activate
fi

cd frontend/
npm run build

cd ../backend/
python -m core.main

