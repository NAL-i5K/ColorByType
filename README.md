# ColorByType
A JBrowse plugin to color the features according the feature type

# Screenshot
![Screenshot](img/screenshot.PNG)

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
