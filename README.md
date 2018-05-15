# Introduction
A JBrowse plugin to color the features according the feature type.

# Screenshot
![](img/screenshot.PNG)
- Several feature types (e.g. mRNA, lncRNA, tRNA) were loaded into one track. The coloring of the exon/CDS boxes is related to the feature type of its parent.

# Requirement
- [color-hash](https://github.com/zenozeng/color-hash)
# Install
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
    - exon `#d7f7c0`![#d7f7c0](https://placehold.it/15/d7f7c0/000000?text=+)
    - CDS `#28db25`![#28db25](https://placehold.it/15/28db25/000000?text=+)
- lnc_RNA
    - exon `#262dff`![#262dff](https://placehold.it/15/262dff/000000?text=+)
- snoRNA
    - exon `#7cedff`![#7cedff](https://placehold.it/15/7cedff/000000?text=+)
- transcript
    - exon `#c589c6`![#c589c6](https://placehold.it/15/c589c6/000000?text=+)
- rRNA
    - exon `#fff200`![#fff200](https://placehold.it/15/fff200/000000?text=+)
- snRNA
    - exon `#80a823`![#80a823](https://placehold.it/15/80a823/000000?text=+)
- tRNA
    - exon `#ef7902`![#ef7902](https://placehold.it/15/ef7902/000000?text=+)
- Others feature types will be colored by color-hash
