# AI Data Analytics Predictor Project for PGA golfer tournament results.

## Recommended Steps to setup:
### Suggested to setup virtual environment
python -m venv .venv
source .venv/bin/activate

## Make sure you are running Python 3.11+
pip install -r requirements.txt

## Install the frontend server packages
cd frontend

npm install

## Start the backend server
cd pga

python manage.py runserver

## You may need to migrate the SqlLite DB if you get warnings:
python manage.py migrate

## Start the frontend server
### rename the frontend/env_sample file to .env
cd frontend

npm run serve

## Navigate to the page:
http://localhost:8080/

