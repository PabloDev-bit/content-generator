#!/bin/bash

python3 -m venv env
source env/bin/activate

pip install --upgrade pip
pip install flask openai requests

echo "Setup terminé."