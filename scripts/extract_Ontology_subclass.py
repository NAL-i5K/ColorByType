#! /usr/bin/env python
# Contributed by Li-Mei Chiang <dytk2134 [at] gmail [dot] com> (2018)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.

import sys
import re
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.handlers:
    lh = logging.StreamHandler()
    lh.setFormatter(logging.Formatter('%(levelname)-8s %(message)s'))
    logger.addHandler(lh)

__version__ = '1.0.0'

def main(args):
    import pronto
    outfilename = os.path.join(args.outdir, 'OS_table.tsv')
    ontology = pronto.Ontology(args.ontology_obo)
    with open(outfilename, 'w') as out_f:
        try:
            # data-version
            outline = '# %s\n' % (' '.join(ontology.meta['data-version']))
            out_f.write(outline)
        except KeyError:
            pass
        # SO_ID SO_term child_term
        for term in ontology:
            child_term_list = list()
            children = term.rchildren()
            for child in children:
                child_term_list.append(child.name)
            outlist = [term.id, term.name, ','.join(child_term_list)]
            outline = '\t'.join(outlist) + '\n'
            out_f.write(outline)
    out_f.close()
if __name__ == '__main__':
    import argparse
    from textwrap import dedent
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description=dedent("""\

    Quick start:
    %(prog)s -obo so.obo -out ColorByType/
    """))


    parser.add_argument('-obo', '--ontology_obo', type=str, help='Ontology OBO files', required=True)
    parser.add_argument('-out', '--outdir', type=str, help='output directory', required=True)
    parser.add_argument('-v', '--version', action='version', version='%(prog)s ' + __version__)

    args = parser.parse_args()
    main(args)