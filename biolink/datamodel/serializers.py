from flask_restplus import fields
from biolink.api.restplus import api


# todo: split this into modules

# Solr

search_result = api.model('SearchResult', {
    'numFound': fields.Integer,
    'start': fields.Integer,
    'facet_counts': fields.Raw
    })

## BBOP/OBO Graphs


node = api.model('Node', {
    'id': fields.String(readOnly=True, description='ID'),
    'lbl': fields.String(readOnly=True, description='RDFS Label')
})

edge = api.model('Edge', {
    'sub': fields.String(readOnly=True, description='Subject Node ID'),
    'pred': fields.String(readOnly=True, description='Predicate (Relation) ID'),
    'obj': fields.String(readOnly=True, description='Subject Node ID'),
})

bbop_graph = api.model('Graph', {
    'nodes': fields.List(fields.Nested(node)),
    'edges': fields.List(fields.Nested(edge)),
})


named_object = api.model('NamedObject', {
    'id': fields.String(readOnly=True, description='ID'),
    'label': fields.String(readOnly=True, description='RDFS Label'),
    'category': fields.String(readOnly=True, description='Type of object')
})

relation = api.inherit('Relation', named_object, {
})

publication = api.inherit('Publication', named_object, {
    # authors etc
})


# todo: inherits
taxon = api.model('Taxon', {
    'id': fields.String(readOnly=True, description='ID'),
    'label': fields.String(readOnly=True, description='RDFS Label')
})

bio_object = api.inherit('BioObject', named_object, {
    'taxon': fields.Nested(taxon)
})


# Assoc

association = api.model('Association', {
    'id': fields.String(readOnly=True, description='Association ID'),
    'subject': fields.Nested(bio_object),
    'object': fields.Nested(bio_object),
    'relation': fields.Nested(relation),
    'evidence_graph': fields.Nested(bbop_graph),
    'provided_by': fields.List(fields.String),
    'publications': fields.List(fields.Nested(publication))
})

association_results = api.inherit('AssociationResults', search_result, {
    'associations': fields.List(fields.Nested(association))
})


# Bio Objects

sequence_position = api.inherit('SequencePosition', bio_object, {
    'position': fields.Integer,
    'reference': fields.String
})

sequence_location = api.inherit('SequenceLocation', bio_object, {
    'begin': fields.Nested(sequence_position),
    'end': fields.Nested(sequence_position),
})

sequence_feature = api.inherit('SequenceFeature', bio_object, {
    'locations': fields.List(fields.Nested(sequence_location)),
    'sequence': fields.String
})

gene = api.inherit('Gene', sequence_feature, {
    'family_ids' : fields.List(fields.String)
})

gene_product = api.inherit('GeneProduct', sequence_feature, {
    'genes': fields.List(fields.Nested(gene))
})

transcript = api.inherit('Transcript', sequence_feature, {
    'genes': fields.List(fields.Nested(gene))
})

genotype = api.inherit('Genotype', sequence_feature, {
    'genes': fields.List(fields.Nested(gene))
})

allele = api.inherit('Allele', sequence_feature, {
    'genes': fields.List(fields.Nested(gene))
})

# molecular entities
molecular_complex = api.inherit('MolecularComplex', bio_object, {
    'genes': fields.List(fields.Nested(gene))
})

drug = api.inherit('Drug', bio_object, {
    'target_associations': fields.List(fields.Nested(association))
})

# phylo
phylogenetic_node = api.inherit('PhylogeneticNode', named_object, {
    'feature': fields.Nested(sequence_feature),
    'parent_id': fields.String,
    'event': fields.String,
    'branch_length': fields.Float
})
phylogenetic_tree = api.inherit('PhylogeneticTree', named_object, {
})

# clinical
clinical_individual = api.inherit('ClinicalIndividual', named_object, {
})
