#Spellchecker API
This is my first API in Python, so I'm sure there are Python naming and other convention violations everywhere. I've made use of the *flask* and *connexion* frameworks to both serve and document the api in Swagger. It also uses *FlaskInjector* for dependency injection.

1. Swagger UI is located at http://localhost:8080/ui
2. Requires Python 3.6
3. App currently runs on default port 5000, which will be overidden to port 8080 by passing the port to flask or using the docker-compose file and docker to run the app (see instructions below)
4. A small set of functional tests are included as a Postman collection as "SpellChecker.postman_collection.json"
4. Unit tests are in tests/test_spellchecker.py, but while they convey the gist of the desired tests I want, they are not currently passing. I am just beginning to learn the built-in Python unittest module vs nose vs pyTest and how to properly mock dependencies.

###To run on a local machine using locally installed Python
pip install -r requirements.txt && flask run -p 8080

###To run in Docker (must have Docker installed, downloads Python docker image)
docker-compose up