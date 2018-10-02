#! /usr/bin/env python
import re
import logging
import subprocess
import shlex

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    lh = logging.StreamHandler()
    lh.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    logger.addHandler(lh)

__version__ = '1.0.0'


def gff_reader(gff):
    # gff_dict = {'CDSA': [{'ID': 'CDSA', 'type': 'CDS', ''attributes': {}}, {'ID': 'CDSA', 'type': 'CDS', 'attributes': {}}]}
    gff_dict = dict()
    # gene_model = {'parentID1': {'1': ['gene'], '2': ['mRNA'], '3':['CDS','exon']}}
    gene_model = dict()
    missing_parent = list()
    with open(gff, 'rb') as in_f:
        for line in in_f:
            line = line.strip()
            # ignore all blank lines, directives and comments
            if len(line) != 0 and not line.startswith('#'):
                tokens = line.split('\t')
                # attributes = {'ID': 'rnaA', 'Name': 'rnaA', 'Parent': 'geneA,geneB'}
                attributes = dict(re.findall('([^=;]+)=([^=;\n]+)', tokens[8]))
                feature = {
                    'ID': None,
                    'type': tokens[2],
                    'level': None,
                    'children': [],
                    'parent': [],
                    'root': None,
                    'attributes': attributes
                }
                find_parent = False
                if 'ID' in attributes:
                    feature['ID'] = attributes['ID']
                    # root, first-level feature
                    if 'Parent' not in attributes:
                        find_parent = True
                        feature['level'] = 1
                        feature['root'] = attributes['ID']
                        gene_model[attributes['ID']] = {
                            1: set()
                        }
                        # first-level feature type
                        gene_model[attributes['ID']][1].add(tokens[2])
                    else:
                        # children of the root
                        # a child feature might have multiple parent
                        # parent_list = ['parentA', 'parentB']
                        parent_list = attributes['Parent'].split(',')
                        attributes['Parent'] = parent_list
                        for p in parent_list:
                            if p in gff_dict:
                                find_parent = True
                                feature['parent'].extend(gff_dict[p])
                                feature['level'] = gff_dict[p][0]['level'] + 1
                                feature['root'] = gff_dict[p][0]['root']
                                # add new level to gene_model
                                if feature['root'] in gene_model:
                                    if feature['level'] not in gene_model[feature['root']]:
                                        gene_model[feature['root']][feature['level']] = set()
                                    gene_model[feature['root']][feature['level']].add(feature['type'])
                                gff_dict[p][0]['children'].append(feature)
                    if find_parent == False:
                        missing_parent.append(feature)
                        continue
                    if attributes['ID'] not in gff_dict:
                        gff_dict[attributes['ID']] = [feature]
                    else:
                        gff_dict[attributes['ID']].append(feature)
                else:
                    # parent feature should have ID attribute
                    if 'Parent' in attributes:
                        parent_list = attributes['Parent'].split(',')
                        attributes['Parent'] = parent_list
                        for p in parent_list:
                            if p in gff_dict:
                                find_parent = True
                                feature['root'] = gff_dict[p][0]['root']
                                feature['level'] = gff_dict[p][0]['level'] + 1
                                if feature['root'] in gene_model:
                                    if feature['level'] not in gene_model[feature['root']]:
                                        gene_model[feature['root']][feature['level']] = set()
                                    gene_model[feature['root']][feature['level']].add(feature['type'])
                        if find_parent == False:
                            missing_parent.append(feature)
                            continue
        for feature in missing_parent:
            for p in feature['attributes']['Parent']:
                if p in gff_dict:
                    feature['parent'].extend(gff_dict[p])
                    feature['root'] = gff_dict[p][0]['root']
                    feature['level'] = gff_dict[p][0]['level'] + 1
                    if feature['root'] in gene_model:
                        if feature['level'] not in gene_model[feature['root']]:
                            gene_model[feature['root']][feature['level']] = set()
                            gene_model[feature['root']][feature['level']].add(feature['type'])
                        gff_dict[p][0]['children'].append(feature)
            if 'ID' in feature['attributes']:
                if attributes['ID'] not in gff_dict:
                    gff_dict[attributes['ID']] = [feature]
                else:
                    gff_dict[attributes['ID']].append(feature)
    return gene_model


def get_loading_types(gff):
    # type in column 3
    loading_types = {
        'first': set(),
        'second': set()
    }
    gff_model = gff_reader(gff)
    for key in gff_model:
        # first-level -> second-level -> third-level (load as second-level feature)
        if len(gff_model[key]) > 2:
            loading_types['second'].update(gff_model[key][2])
        else:
            # first-level -> second-level (load as first-level feature)
            # currently, only pseudogene load as first-level features
            if 'pseudogene' in gff_model[key][1]:
                loading_types['first'].add('pseudogene')
    return loading_types

def main(args):
    # get first-level and second-level feature types
    loading_types = get_loading_types(args.gff_file)
    # NCBI flatfile-to-json.pl command template
    # required arguments: --out, --gff, --type
    # option: --clientConfig

    template = "perl %(flatfile_to_json)s --clientConfig %(clientConfig)s --trackType %(trackType)s --out %(data)s --gff %(gff)s --arrowheadClass %(arrowheadClass)s %(getSubfeatures)s --subfeatureClasses %(subfeatureClasses)s --cssClass %(cssClass)s --type %(type)s --trackLabel %(trackLabel)s --key %(key)s --config %(config)s"
    template_init = {
    'flatfile_to_json': args.path_to_flatfile_to_json,
    'data': args.out,
    'gff': args.gff_file,
    'trackLabel': "",
    'key' : "",
    'clientConfig': "\'{ \"description\": \"product, note, description\" }\'",
    'arrowheadClass': "trellis-arrowhead",
    'getSubfeatures': "--getSubfeatures",
    'subfeatureClasses': "\'{\"wholeCDS\": null, \"CDS\":\"gnomon_CDS\", \"UTR\": \"gnomon_UTR\", \"exon\":\"container-100pct\"}\'",
    'cssClass': "container-16px",
    'config': "",
    'type': "",
    'trackType': 'HTMLFeatures'
    }
    config_template = "\'{ \"category\": \"NCBI Annotation Release %(version)s\" , \"metadata\": {\"Data description\": \"ftp://ftp.ncbi.nlm.nih.gov/genomes/%(Genus_species)s/README_CURRENT_RELEASE\", \"Data source\": \"%(link)s\", \"Data provider\": \"NCBI\", \"Method\": \"http://www.ncbi.nlm.nih.gov/genome/annotation_euk/process/\"}}\'"
    config_init = {
        'version': args.release_version,
        'key': '',
        'Genus_species': args.organism,
        'link': args.data_source
    }
    if args.config:
        template_init['config'] = args.config

    # NCBI release genes
    ## get second-level features
    if not args.trackLabel_gene:
        args.trackLabel_gene = 'NCBI_Annotation_Release_%s_Gene' % (args.release_version)
    template_init['trackLabel'] = args.trackLabel_gene
    if not args.key_gene:
        template_init['key'] = 'NCBI_Annotation_Release_%s_Gene' % (args.release_version)
    else:
        template_init['key'] = args.key_gene
    template_init['type'] = ','.join(list(loading_types['second']))
    # Jbrowse plugin: ColorByType
    template_init['trackType'] = 'ColorByType/View/Track/ColorByTypeDraggable'
    if not args.config:
        config_init['key'] = template_init['key']
        template_init['config'] = config_template % config_init
    cmd = shlex.split(template % template_init)
    if len(loading_types['second']) > 0:
        logger.info('Running command: (%s)' % (template % template_init))
        subprocess.Popen(cmd).wait()

    # NCBI release pseudogenes
    ## get first-level features
    if not args.trackLabel_psudogene:
        args.trackLabel_psudogene = 'NCBI_Annotation_Release_%s_Pseudogene' % (args.release_version)
    template_init['trackLabel'] = args.trackLabel_psudogene
    if not args.key_psudogene:
        template_init['key'] = 'NCBI_Annotation_Release_%s_Pseudogene' % (args.release_version)
    else:
        template_init['key'] = args.key_psudogene
    template_init['type'] = ','.join(list(loading_types['first']))
    template_init['trackType'] = 'HTMLFeatures'
    if not args.config:
        config_init['key'] = template_init['key']
        template_init['config'] = config_template % config_init
    cmd = shlex.split(template % template_init)
    if len(loading_types['first']) > 0:
        logger.info('Running command: (%s)' % (template % template_init))
        subprocess.Popen(cmd).wait()
    # trackList = os.path.join(args.out, 'trackList.json')
    # Add_javascript(trackList, args.trackLabel_gene, args.trackLabel_psudogene, loading_types)

if __name__ == '__main__':
    import argparse
    from textwrap import dedent
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=dedent("""\


    Quick start:
    %(prog)s -path Apollo/bin/flatfile-to-json.pl -gff test.gff -out jbrowse/data/ -organism Leptinotarsa_decemlineata -release 100 -source ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/500/325/GCF_000500325.1_Ldec_2.0/GCF_000500325.1_Ldec_2.0_genomic.gff.gz
    """))


    parser.add_argument('-path', '--path_to_flatfile_to_json', type=str, help='Path to flatfile-to-json.pl', required=True)
    parser.add_argument('-gff', '--gff_file', type=str, help='Gff3 file', required=True)
    parser.add_argument('-out', '--out', type=str, help='out', required=True)
    parser.add_argument('-key1', '--key_gene', type=str, help='human-readable track name for genes.')
    parser.add_argument('-key2', '--key_psudogene', type=str, help='human-readable track name for pseudogenes.')
    parser.add_argument('-trackLabel1', '--trackLabel_gene', type=str, help='track identifier for genes.')
    parser.add_argument('-trackLabel2', '--trackLabel_psudogene', type=str, help='track identifier for pseudogenes.',)
    parser.add_argument('-organism', '--organism', type=str, help='Genus_species')
    parser.add_argument('-config', '--config', type=str, help='{ JSON-format extra configuration for this track }')
    parser.add_argument('-clientConfig', '--clientConfig', type=str, help='{ JSON-format style configuration for this track }')
    parser.add_argument('-subfeatureCkasses', '--subfeatureClasses', type=str, help='{ JSON-format subfeature class }')
    parser.add_argument('-nogetSubfeatures', '--nogetSubfeatures', action='store_true', help='don\'t get sub-features', default=False)
    parser.add_argument('-release', '--release_version',type=str, help='NCBI Annotation Release version', default="")
    parser.add_argument('-source', '--data_source',type=str, help='link to gff on NCBI website', default="")
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()
    main(args)

