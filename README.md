# Introduction
A JBrowse plugin to color the features according the feature type.

# Screenshot
![](img/screenshot.PNG)
- Several feature types (e.g. mRNA, lncRNA, tRNA) were loaded into one track. The coloring of the exon/CDS boxes is related to the feature type of its parent.

# Requirement
- [color-hash](https://github.com/zenozeng/color-hash)
# Install
## Node.js
`npm install color-hash`

## ColorByType
Download to plugins/ColorByType and change the type to `ColorByType/View/Track/ColorByType`
```
     {
         "category" : "NCBI Annotation Release 100/1. Gene Sets/NCBI_Annotation_Release_100_Gene",
         "key" : "NCBI_Annotation_Release_100_Gene",
         "label" : "NCBI_Annotation_Release_100_Gene",
         "trackType" : null,
         "type" : "ColorByType/View/Track/ColorByType",
         "urlTemplate" : "tracks/NCBI_Annotation_Release_100_Gene/{refseq}/trackData.json"
      },
```

## The coloring of the common feature types
- mRNA
    - exon ```#d7f7c0```
    - CDS ```#28db25```
- lnc_RNA
    - exon ```#262dff```
- snoRNA
    - exon ```#7cedff```
- transcript
    - exon ```#c589c6```
- rRNA
    - exon ```#fff200```
- snRNA
    - exon ```#80a823```
- tRNA
    - exon ```#ef7902```
- Others feature types will be colored by color-hash