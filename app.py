import connexion
from flask_injector import FlaskInjector
from services.spellcheck_dictionary import SpellCheckDictionary
from conf.settings import settings


# inject the dictionary
def configure(binder):
    binder.bind(
        SpellCheckDictionary,
        SpellCheckDictionary().fromUrl(settings["dictionary-url"])
    )

# load the swagger definition
app = connexion.App(__name__, specification_dir='./swagger/')
app.add_api('swagger.yml')
application = app.app

FlaskInjector(app=app.app, modules=[configure])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
