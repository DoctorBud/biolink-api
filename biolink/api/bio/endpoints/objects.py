import logging

from flask import request
from flask_restplus import Resource
from biolink.datamodel.serializers import association_results, association, gene, drug, genotype, allele, search_result
#import biolink.datamodel.serializers
from biolink.api.restplus import api
from biolink.util.golr_associations import search_associations
import pysolr

log = logging.getLogger(__name__)

ns = api.namespace('bio', description='Retrieval of domain objects plus associations')

core_parser = api.parser()
core_parser.add_argument('exclude_evidence', type=bool, help='If set, excludes evidence objects in response')

@ns.route('/gene/<id>')
@api.doc(params={'id': 'id, e.g. NCBIGene:84570'})
class GeneObject(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(gene)
    def get(self, id):
        """
        TODO Returns gene object
        """
        return { 'foo' : 'bar' }

@api.doc(params={'id': 'id, e.g. NCBIGene:3630. Equivalent IDs can be used with same results'})
class AbstractGeneAssociationResource(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        pass
    
@ns.route('/gene/<id>/interactions/')
class GeneInteractions(AbstractGeneAssociationResource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns interactions for a gene
        """
        return search_associations('gene', 'gene', 'RO:0002434', id, **core_parser.parse_args())

homolog_parser = api.parser()
homolog_parser.add_argument('homolog_taxon', help='Taxon CURIE of homolog, e.g. NCBITaxon:9606. Can be intermediate note, includes inferred by default')
homolog_parser.add_argument('type', help='P, O or LDO (paralog, ortholog or least-diverged), or corresponding RO ID')

@ns.route('/gene/<id>/homologs/')
class GeneHomologAssociations(AbstractGeneAssociationResource):

    @api.expect(homolog_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns homologs for a gene
        """
        rel = 'RO:0002434'  # TODO
        return search_associations('gene', 'gene', rel, id, **core_parser.parse_args())
    
@ns.route('/gene/<id>/phenotypes/')
@api.doc(params={'id': 'CURIE identifier of gene, e.g. NCBIGene:4750. Equivalent IDs can be used with same results'})
class GenePhenotypeAssociations(Resource):

    @api.expect(core_parser)
    def get(self, id):
        """
        Returns phenotypes associated with gene
        """
        args = core_parser.parse_args()
        print(args)

        return search_associations('gene', 'phenotype', None, id, **core_parser.parse_args())

@ns.route('/gene/<id>/expressed/')
@api.doc(params={'id': 'CURIE identifier of gene, e.g. NCBIGene:4750. Equivalent IDs can be used with same results'})
class GeneExpressionAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        TODO Returns expression events for a gene
        """

        return search_associations('gene', 'anatomy', None, id, **core_parser.parse_args())

@ns.route('/gene/<id>/pubs/')
@api.doc(params={'id': 'CURIE identifier of gene, e.g. NCBIGene:4750. Equivalent IDs can be used with same results'})
class GenePublicationList(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        TODO Returns expression events for a gene
        """

        # TODO: we don't store this directly
        # could be retrieved by getting all associations and then extracting pubs
        return search_associations('gene', 'publication', None, id, **core_parser.parse_args())
    
@ns.route('/geneproduct/<id>')
class GeneproductObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns gene product object
        """
        return { 'foo' : 'bar' }
    
@ns.route('/disease/<id>')
class DiseaseObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns disease object
        """
        return { 'foo' : 'bar' }

@ns.route('/disease/<id>/phenotypes/')
@api.doc(params={'id': 'CURIE identifier of disease, e.g. OMIM:605543, DOID:678. Equivalent IDs can be used with same results'})
class DiseasePhenotypeAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns phenotypes associated with disease
        """

        return search_associations('disease', 'phenotype', None, id, **core_parser.parse_args())

@ns.route('/disease/<id>/genes/')
@api.doc(params={'id': 'CURIE identifier of disease, e.g. OMIM:605543, DOID:678. Equivalent IDs can be used with same results'})
class DiseaseGeneAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns genes associated with a disease
        """
        args = core_parser.parse_args()
        print(args)

        return search_associations('disease', 'gene', None, id, **core_parser.parse_args())

@ns.route('/disease/<id>/anatomy/')
class DiseaseAnatomyAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns anatomical locations associated with a phenotype
        """
        return { 'foo' : 'bar' }
    
@ns.route('/disease/<id>/models/')
@api.doc(params={'id': 'CURIE identifier of disease, e.g. OMIM:605543, DOID:678. Equivalent IDs can be used with same results'})
class DiseaseModelAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        TODO Returns models associated with a disease
        """

        # TODO: invert
        return search_associations('model', 'disease', None, id, **core_parser.parse_args())
    
@ns.route('/phenotype/<id>')
class PhenotypeObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns phenotype class object
        """
        return { 'foo' : 'bar' }
    
@ns.route('/phenotype/<id>/anatomy/')
class PhenotypeAnatomyAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns anatomical locations associated with a phenotype
        """
        return { 'foo' : 'bar' }

@ns.route('/phenotype/<id>/phenotype/')
class PhenotypePhenotypeAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns associated phenotypes

        Includes phenologs, as well as equivalent phenotypes in other species
        """
        return { 'foo' : 'bar' }
    
@ns.route('/goterm/<id>')
class GotermObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns GO class object
        """
        return { 'foo' : 'bar' }

@ns.route('/pathway/<id>')
@api.doc(params={'id': 'CURIE any pathway element. May be a GO ID or a pathway database ID'})
class PathwayObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns pathway object
        """
        return { 'foo' : 'bar' }
    
@ns.route('/pathway/<id>/genes/')
class PathwayGeneAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of associations
        """
        return { 'foo' : 'bar' }

@ns.route('/pathway/<id>/participants/')
class PathwayParticipantAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns associations to participants (molecules, etc) for a pathway
        """
        return { 'foo' : 'bar' }
    
@ns.route('/anatomy/<id>')
class AnatomyObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of objects
        """
        return { 'foo' : 'bar' }

@ns.route('/anatomy/<id>/genes/')
class AnatomyGeneAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of associations
        """
        return { 'foo' : 'bar' }

@ns.route('/anatomy/<id>/phenotypes/')
class AnatomyPhenotypeAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of associations
        """
        return { 'foo' : 'bar' }
    

@ns.route('/environment/<id>')
class EnvironmentObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of objects
        """
        return { 'foo' : 'bar' }
    
@ns.route('/environment/<id>/phenotypes/')
class EnvironmentPhenotypeAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of associations
        """
        return { 'foo' : 'bar' }

@ns.route('/drug/<id>')
class DrugObject(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(drug)
    def get(self, id):
        """
        TODO Returns list of associations
        """
        return { 'foo' : 'bar' }

@ns.route('/drug/<id>/targets/')
class DrugTargetAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of associations
        """
        return { 'foo' : 'bar' }

@ns.route('/drug/<id>/interactions/')
class DrugInteractions(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of associations
        """
        return { 'foo' : 'bar' }
    
@ns.route('/chemical/<id>')
class ChemicalObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of objects
        """
        return { 'foo' : 'bar' }
    

@ns.route('/genotype/<id>')
class GenotypeObject(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(genotype)
    def get(self, id):
        """
        TODO Returns list of objects
        """
        return { 'foo' : 'bar' }

@ns.route('/genotype/<id>/genotypes/')
@api.doc(params={'id': 'CURIE identifier of genotype, e.g. ZFIN:ZDB-FISH-150901-6607'})
class GenotypeGenotypeAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns genotypes associated with a genotype
        """

        # TODO: invert
        return search_associations('genotype', 'genotype', None, id, **core_parser.parse_args())

@ns.route('/genotype/<id>/phenotypes/')
@api.doc(params={'id': 'CURIE identifier of genotype, e.g. ZFIN:ZDB-FISH-150901-6607'})
class GenotypePhenotypeAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns phenotypes associated with a genotype
        """

        # TODO: invert
        return search_associations('genotype', 'phenotypes', None, id, **core_parser.parse_args())
    
@ns.route('/genotype/<id>/genes/')
@api.doc(params={'id': 'CURIE identifier of genotype, e.g. ZFIN:ZDB-FISH-150901-6607'})
class GenotypeGeneAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns genes associated with a genotype
        """

        # TODO: invert
        return search_associations('genotype', 'gene', None, id, **core_parser.parse_args())

##

@ns.route('/allele/<id>')
class AlleleObject(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(allele)
    def get(self, id):
        """
        TODO Returns allele object

        This is a composition of multiple smaller operations,
        including fetching allele metadata, plus allele associations

        TODO - should allele be subsumed into variant?
        """
        return { 'id' : 'foobar' }
    

@ns.route('/variant/<id>')
@api.doc(params={'id': 'CURIE identifier of variant, e.g. ZFIN:ZDB-ALT-010427-8'})
class VariantObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of objects
        """
        return { 'foo' : 'bar' }

@ns.route('/variant/<id>/genotypes/')
@api.doc(params={'id': 'CURIE identifier of variant, e.g. ZFIN:ZDB-ALT-010427-8'})
class VariantGenotypeAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns genotypes associated with a variant
        """

        # TODO: invert
        return search_associations('variant', 'genotype', None, id, **core_parser.parse_args())

@ns.route('/variant/<id>/phenotypes/')
@api.doc(params={'id': 'CURIE identifier of variant, e.g. ZFIN:ZDB-ALT-010427-8'})
class VariantPhenotypeAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns phenotypes associated with a variant
        """

        # TODO: invert
        return search_associations('variant', 'phenotypes', None, id, **core_parser.parse_args())
    
@ns.route('/variant/<id>/genes/')
@api.doc(params={'id': 'CURIE identifier of variant, e.g. ZFIN:ZDB-ALT-010427-8'})
class VariantGeneAssociations(Resource):

    @api.expect(core_parser)
    @api.marshal_list_with(association_results)
    def get(self, id):
        """
        Returns genes associated with a variant
        """

        # TODO: invert
        return search_associations('variant', 'gene', None, id, **core_parser.parse_args())
    
@ns.route('/sequence_feature/<id>')
class SequenceFeatureObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of objects
        """
        return { 'foo' : 'bar' }


@ns.route('/patient/<id>')
class ParentObject(Resource):

    @api.expect(core_parser)
    #@api.marshal_list_with(association)
    def get(self, id):
        """
        TODO Returns list of objects
        """
        return { 'foo' : 'bar' }


