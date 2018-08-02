#Notes
This project is my first API webservice in Python, so I'm sure there are Python naming and other convention violations everywhere. I've made use of flask and connexion to both serve and document the api in Swagger. 

1. Swagger UI is located at http://localhost:8080/ui
2. Requires Python 3.6
3. App currently runs on default port 5000, will need to be overwritten to port 8080 (instructions below)
4. Unit tests are in tests/test_spellchecker.py, while they convey the gist of the desired test, are not currently passing as I am just beginning the built-in Python unittest module

#To run on a local machine using default Python
pip install -r requirements.txt && flask run -p 8080

#To run in Docker (must have Docker installed, downloads Python docker image)
docker-compose up