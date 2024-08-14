#!/bin/bash

set -eo pipefail

npm run build
if [ -z $VIRTUAL_ENV ]; then
  source venv/bin/activate
fi
cd backend/
python -m core.main

