import logging.config

from flask import Flask, Blueprint
from biolink import settings
from biolink.api.link.endpoints.links import ns as link_search_namespace
from biolink.api.bio.endpoints.objects import ns as bio_objects_namespace
from biolink.api.entity.endpoints.search import ns as bio_objects_namespace
from biolink.api.nlp.endpoints.annotate import ns as nlp_annotate_namespace
from biolink.api.ontol.endpoints.slimmer import ns as ontol_slimmer_namespace
from biolink.api.ontol.endpoints.enrichment import ns as ontol_enrichment_namespace
from biolink.api.lego.endpoints.model import ns as lego_model_namespace
from biolink.api.owl.endpoints.ontology import ns as owl_ontology_namespace
from biolink.api.patient.endpoints.individual import ns as patient_individual_namespace
from biolink.api.identifier.endpoints.prefixes import ns as identifier_prefixes_namespace
from biolink.api.identifier.endpoints.mapper import ns as identifier_prefixes_mapper

from biolink.api.evidence.endpoints.graph import ns as evidence_graph_namespace

from biolink.api.variation.endpoints.variantset import ns as variation_variantset_namespace

from biolink.api.restplus import api

from biolink.database import db

app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(link_search_namespace)
    flask_app.register_blueprint(blueprint)

    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
