import logging

from flask import request, send_file
from flask_restplus import Resource
from biolink.datamodel.serializers import association, bbop_graph
from biolink.util.golr_associations import get_association
from biolink.api.restplus import api
from biolink.core.ontology.obograph_util import convert_json_object
import tempfile
import pysolr
import matplotlib.pyplot as plt
import networkx as nx

log = logging.getLogger(__name__)

ns = api.namespace('evidence/graph', description='Operations on evidence graphs')

parser = api.parser()
#parser.add_argument('subject_taxon', help='SUBJECT TAXON id, e.g. NCBITaxon:9606. Includes inferred by default')

@ns.route('/<id>')
@api.doc(params={'id': 'association id, e.g. cfef92b7-bfa3-44c2-a537-579078d2de37'})
class AssociationObject(Resource):

    @api.expect(parser)
    @api.marshal_list_with(bbop_graph)
    def get(self,id):
        """
        Returns evidence graph object for a given association.

        Note that every association is assumed to have a unique ID
        """
        args = parser.parse_args()

        assoc = get_association(id)
        eg = assoc.get('evidence_graph')
        return [eg]

@ns.route('/<id>/image')
class AssociationObject(Resource):

    @api.expect(parser)
    def get(self,id):
        """
        Returns evidence graph as a png
        """
        args = parser.parse_args()

        assoc = get_association(id)
        eg = {'graphs':[assoc.get('evidence_graph')]}
        digraph = convert_json_object(eg)
        #fp = tempfile.TemporaryFile()
        nx.draw(digraph)
        fn = '/tmp/'+id+'.png' # TODO
        plt.savefig(fn)
        return send_file(fn)
        
    


    
    

