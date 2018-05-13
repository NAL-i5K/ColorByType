# Load NCBI annotation
## Background
There are many different transcript type information stored in a NCBI's eukaryotic annotation pipeline gff3 files. The add_NCBI_annotation_track.py aims to help scientist load those data to Jbrowse. This script will read the gff3 files and decide a model should be loaded as 2nd-level features or 1st-feature.

## Prerequisite
- python

## Usage
### help and usage messages
```
usage: add_javescript_to_json.py [-h] -path PATH_TO_FLATFILE_TO_JSON -gff
                                 GFF_FILE -out OUT [-key1 KEY_GENE]
                                 [-key2 KEY_PSUDOGENE]
                                 [-trackLabel1 TRACKLABEL_GENE]
                                 [-trackLabel2 TRACKLABEL_PSUDOGENE]
                                 [-organism ORGANISM] [-config CONFIG]
                                 [-clientConfig CLIENTCONFIG]
                                 [-subfeatureCkasses SUBFEATURECLASSES]
                                 [-nogetSubfeatures]
                                 [-release RELEASE_VERSION]
                                 [-source DATA_SOURCE] [-v]

Quick start:
add_javescript_to_json.py -path Apollo/bin/flatfile-to-json.pl -gff test.gff -out jbrowse/data/ -organism Leptinotarsa_decemlineata -release 100 -source ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/500/325/GCF_000500325.1_Ldec_2.0/GCF_000500325.1_Ldec_2.0_genomic.gff.gz

optional arguments:
  -h, --help            show this help message and exit
  -path PATH_TO_FLATFILE_TO_JSON, --path_to_flatfile_to_json PATH_TO_FLATFILE_TO_JSON
                        Path to flatfile-to-json.pl
  -gff GFF_FILE, --gff_file GFF_FILE
                        Gff3 file
  -out OUT, --out OUT   out
  -key1 KEY_GENE, --key_gene KEY_GENE
                        human-readable track name for genes.
  -key2 KEY_PSUDOGENE, --key_psudogene KEY_PSUDOGENE
                        human-readable track name for pseudogenes.
  -trackLabel1 TRACKLABEL_GENE, --trackLabel_gene TRACKLABEL_GENE
                        track identifier for genes.
  -trackLabel2 TRACKLABEL_PSUDOGENE, --trackLabel_psudogene TRACKLABEL_PSUDOGENE
                        track identifier for pseudogenes.
  -organism ORGANISM, --organism ORGANISM
                        Genus_species
  -config CONFIG, --config CONFIG
                        { JSON-format extra configuration for this track }
  -clientConfig CLIENTCONFIG, --clientConfig CLIENTCONFIG
                        { JSON-format style configuration for this track }
  -subfeatureCkasses SUBFEATURECLASSES, --subfeatureClasses SUBFEATURECLASSES
                        { JSON-format subfeature class }
  -nogetSubfeatures, --nogetSubfeatures
                        don't get sub-features
  -release RELEASE_VERSION, --release_version RELEASE_VERSION
                        NCBI Annotation Release version
  -source DATA_SOURCE, --data_source DATA_SOURCE
                        link to gff on NCBI website
  -v, --version         show program's version number and exit
  ```
### Introduction
This script will read the gff3 files and decide a model should be loaded as 2nd-level features or 1st-feature. If a model contains more than two level features, this model will be loaded as 2nd-level features; If a model contains less than two level features, then this model will be loaded as 1st-level features. Currently, only pseudogene will be load as 1st-level features.
#### example
```
NW_019289416.1  Gnomon  gene    138305  145237  .       -       .       ID=gene8;Dbxref=GeneID:111510127;Name=LOC111510127;gbkey=Gene;gene=LOC111510127;gene_biotype=protein_coding
NW_019289416.1  Gnomon  mRNA    138305  145237  .       -       .       ID=rna15;Parent=gene8;Dbxref=GeneID:111510127,Genbank:XM_023166344.1;Name=XM_023166344.1;gbkey=mRNA;gene=LOC111510127;model_evidence
=Supporting evidence includes similarity to: 100%25 coverage of the annotated genomic feature by RNAseq alignments%2C including 59 samples with support for all annotated introns;product=uncharacterized LO
C111510127;transcript_id=XM_023166344.1
NW_019289416.1  Gnomon  exon    145129  145237  .       -       .       ID=id111;Parent=rna15;Dbxref=GeneID:111510127,Genbank:XM_023166344.1;gbkey=mRNA;gene=LOC111510127;product=uncharacterized LOC1115101
27;transcript_id=XM_023166344.1
NW_019289416.1  Gnomon  CDS     145129  145161  .       -       0       ID=cds14;Parent=rna15;Dbxref=GeneID:111510127,Genbank:XP_023022112.1;Name=XP_023022112.1;gbkey=CDS;gene=LOC111510127;product=unchara
cterized protein LOC111510127;protein_id=XP_023022112.1
###
NW_019289416.1  Gnomon  pseudogene      404214  405047  .       +       .       ID=gene24;Dbxref=GeneID:111517572;Name=LOC111517572;gbkey=Gene;gene=LOC111517572;gene_biotype=pseudogene;pseudo=true
NW_019289416.1  Gnomon  exon    404214  405047  .       +       .       ID=id158;Parent=gene24;Dbxref=GeneID:111517572;gbkey=exon;gene=LOC111517572;model_evidence=Supporting evidence includes similarity to: 19 Proteins%2C and 53%25 coverage of the annotated genomic feature by RNAseq alignments
###
NW_019289416.1  tRNAscan-SE     gene    479582  479653  .       -       .       ID=gene25;Dbxref=GeneID:111517991;Name=Trnap-cgg;gbkey=Gene;gene=Trnap-cgg;gene_biotype=tRNA
NW_019289416.1  tRNAscan-SE     tRNA    479582  479653  .       -       .       ID=rna30;Parent=gene25;Dbxref=GeneID:111517991;Note=transfer RNA proline (anticodon CGG);anticodon=(pos:complement(479619..479621));gbkey=tRNA;gene=Trnap-cgg;inference=COORDINATES: profile:tRNAscan-SE:1.23;product=tRNA-Pro
NW_019289416.1  tRNAscan-SE     exon    479582  479653  .       -       .       ID=id159;Parent=rna30;Dbxref=GeneID:111517991;Note=transfer RNA proline (anticodon CGG);anticodon=(pos:complement(479619..479621));gbkey=tRNA;gene=Trnap-cgg;inference=COORDINATES: profile:tRNAscan-SE:1.23;product=tRNA-Pro
```
- Both gene8 and gene25 contain more than two level features. Therefore, these two models will be loaded as 2nd-level features which means gene8 will be loaded with mRNA -> exon/CDS; gene25 will be loaded with tRNA -> exon.
- gene24 contains less than two level features. This models will be loaded as 1st-level feature. (pseudogene -> exon)

#### assumption
- The hierarchy of a feature type in a gff3 file is always the same (e.g. mRNA is always a 2nd-level feature).
- If a children feature has multiple parents, then all its parent should be in the same hierarchy.
- If there are features with duplicate ID in the gff3 file, all these features should be in the same hierarchy.

#### default setting
- key1 KEY_GENE, --key_gene KEY_GENE
    - default: NCBI_Annotation_Release_[release_version]_Gene
- key2 KEY_PSUDOGENE, --key_psudogene KEY_PSUDOGENE
    - default: NCBI_Annotation_Release_[release_version]_Pseudogene
- trackLabel1 TRACKLABEL_GENE, --trackLabel_gene TRACKLABEL_GENE
    - default: NCBI_Annotation_Release_[release_version]_Gene
- trackLabel2 TRACKLABEL_PSUDOGENE, --trackLabel_psudogene TRACKLABEL_PSUDOGENE
    - default: NCBI_Annotation_Release_[release_version]_Pseudogene
- config CONFIG, --config CONFIG
    - default:
```
'{ "category": "NCBI Annotation Release [release_version]/1. Gene Sets/[key_gene/key_pseudogene]" , "metadata": {"Data description": "ftp://ftp.ncbi.nlm.nih.gov/genomes/[Genus_species]/README_CURRENT_RELEASE", "Data source": "[data_source]", "Data provider": "NCBI", "Method": "http://www.ncbi.nlm.nih.gov/genome/annotation_euk/process/"}}'
```
- clientConfig CLIENTCONFIG, --clientConfig CLIENTCONFIG
    - default:
```
'{ "description": "product, note, description" }'
```
- subfeatureCkasses SUBFEATURECLASSES, --subfeatureClasses SUBFEATURECLASSES
    - default:
```
'{"wholeCDS": null, "CDS":"gnomon_CDS", "UTR": "gnomon_UTR", "exon":"container-100pct"}'
```