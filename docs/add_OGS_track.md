# Load OGS annotations

There are many different transcript type information stored in a gff3 files and this script aims to help scientist load those data to Jbrowse.
**add_OGS_track.py** will read the gff3 files and decide a model should be loaded as 2nd-level features or 1st-feature and then run **flatfile-to-json.pl** to format the track for JBrowse.
Currently, only **sequence_alteration** and **pseudogene** will be loaded as 1st-level features. For the other feature types contains more than two level features in its model, this model will be loaded as 2nd-level features. By default, **pseudogene** will be loaded in to the track `OGSv[release version number] Pseudogene`; **sequence_alteration** and the other feature types will be loaded to the track `OGSv[release version number] Gene`.

## Prerequisite

- python
- perl
- [ColorByType](https://github.com/NAL-i5K/ColorByType)

## Usage

### help and usage messages

```
usage: add_OGS_track.py [-h] -path PATH_TO_FLATFILE_TO_JSON -gff GFF_FILE -out
                        OUT [-key1 KEY_GENE] [-key2 KEY_PSUDOGENE]
                        [-trackLabel1 TRACKLABEL_GENE]
                        [-trackLabel2 TRACKLABEL_PSUDOGENE]
                        [-organism ORGANISM] [-config CONFIG]
                        [-clientConfig CLIENTCONFIG]
                        [-subfeatureCkasses SUBFEATURECLASSES]
                        [-nogetSubfeatures] [-release RELEASE_VERSION] [-v]

Quick start:
add_OGS_track.py -path Apollo/bin/flatfile-to-json.pl -gff test.gff -out jbrowse/data/ -organism Leptinotarsa_decemlineata -trackLabel1 lepdec_current_models -release 1.2

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
                        Annotation Release version
  -v, --version         show program's version number and exit

```

## example

```
NW_020311285.1  OGSv1.0 gene    34782   38861   .       +       .       ID=AROS004548
NW_020311285.1  OGSv1.0 mRNA    34782   38861   .       +       .       ID=AROS004548-RA;Parent=AROS004548;
NW_020311285.1  OGSv1.0 exon    34782   36198   .       +       .       ID=AROS004548-RA-EXON01;Parent=AROS004548-RA;
NW_020311285.1  OGSv1.0 exon    36766   38861   .       +       .       ID=AROS004548-RA-EXON02;Parent=AROS004548-RA;
NW_020311285.1  OGSv1.0 polypeptide     34782   38861   .       +       .       ID=AROS004548-PA;Parent=AROS004548-RA;
NW_020311285.1  OGSv1.0 CDS     34782   36198   .       +       0       ID=AROS004548-RA-CDS;Parent=AROS004548-RA;
NW_020311285.1  OGSv1.0 CDS     36766   38861   .       +       2       ID=AROS004548-RA-CDS;Parent=AROS004548-RA;
###
NW_020311304.1  OGSv1.0 sequence_alteration     298036  298036  .       +       .       ID=17ed65d8-a109-11e8-8088-9bf0d4d1ab97;Description=insertion;
NW_020311304.1  OGSv1.0 insertion       298036  298036  .       +       .       ID=AROS009859;seq=GA;residues=GA;Parent=17ed65d8-a109-11e8-8088-9bf0d4d1ab97;
###
NW_020311285.1  OGSv1.0 pseudogene    149650  149722  .       +       .       ID=AROS004556;
NW_020311285.1  OGSv1.0 pseudogenic_transcript    149650  149722  .       +       .       Parent=AROS004556;ID=AROS004556-RA
NW_020311285.1  OGSv1.0 pseudogenic_exon    149650  149722  .       +       .       Parent=AROS004556-RA;ID=AROS004556-RA-EXON01
###
```

- **sequence_alteration** and **pseudogene** will be loaded as 1st-level features which means they will be loaded with **sequence_alteration -> insertion** and **pseudogene -> pseudogenic_transcript -> pseudogenic_exon**.
- AROS004548 contain more than two level features and its 1st-level feature is not sequence_alteration or pseudogene. Therefore, this model will be loaded as 1st-level feature which means it will be loaded with **mRNA -> exon/CDS/polypeptide**

## assumption

- The hierarchy of a feature type in a gff3 file is always the same (e.g. mRNA is always a 2nd-level feature).
- If a children feature has multiple parents, then all its parent should be in the same hierarchy.
- If there are features with duplicate ID in the gff3 file, all these features should be in the same hierarchy.

## default setting
- key1 KEY_GENE, --key_gene KEY_GENE
    - default: OGSv[release_version] Gene
- key2 KEY_PSUDOGENE, --key_psudogene KEY_PSUDOGENE
    - default: OGSv[release_version] Pseudogene
- trackLabel1 TRACKLABEL_GENE, --trackLabel_gene TRACKLABEL_GENE
    - default: OGSv[release_version]_Gene
- trackLabel2 TRACKLABEL_PSUDOGENE, --trackLabel_psudogene TRACKLABEL_PSUDOGENE
    - default: OGSv[release_version]_Pseudogene
- config CONFIG, --config CONFIG
    - default: `'{ "category": "Official Gene Set"}'`
- clientConfig CLIENTCONFIG, --clientConfig CLIENTCONFIG
    - default: `'{ "description": "product, note, description" }'`
- subfeatureClasses SUBFEATURECLASSES, --subfeatureClasses SUBFEATURECLASSES
    - default: `'{"wholeCDS": null, "CDS":"gnomon_CDS", "UTR": "gnomon_UTR", "exon":"container-100pct"}'`
