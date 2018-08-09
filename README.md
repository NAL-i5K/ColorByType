# ColorByType

## Introduction

A JBrowse plugin uses [color-hash](https://github.com/zenozeng/color-hash) to color the features according the feature type. This plugin is derived from the [Apollo](https://github.com/GMOD/Apollo) plugin **DraggableHTMLFeatures**.

## Screenshot

![](img/screenshot.PNG)
- Several feature types (e.g. mRNA, lncRNA, tRNA) were loaded into one track. The coloring of the exon/CDS boxes is related to the feature type of its parent.

## Installation

Download to plugins/ColorByType and add a plugins configuration variable in your **jbrowse_conf.json** or **trackList.json**.(see [JBrowse FAQ](http://gmod.org/wiki/JBrowse_FAQ#Plugins) for more detail)
```shell
"plugins": ["ColorByType"]
```

## Usage
- For an existing track, edit the **trackList.json** and change `"type": "[trackType]"` to `"type": "ColorByType/View/Track/ColorByTypeDraggable"`

### Example
```shell
     {
         "category" : "NCBI Annotation Release 100/1. Gene Sets/NCBI_Annotation_Release_100_Gene",
         "key" : "NCBI_Annotation_Release_100_Gene",
         "label" : "NCBI_Annotation_Release_100_Gene",
         "trackType" : null,
         "type" : "ColorByType/View/Track/ColorByTypeDraggable",
         "urlTemplate" : "tracks/NCBI_Annotation_Release_100_Gene/{refseq}/trackData.json"
      },
```
- For a non-existing track, if you load data with **flatfile-to-json.pl**, you can augment the **--trackType** argument with `ColorByType/View/Track/ColorByTypeDraggable`.
- For loading NCBI release annotation to Jbrowse, you can use [add_NCBI_annotation_track.py](scripts/add_NCBI_annotation_track.py) to help you load multiple feature types from the GFF into one track. (check [here](docs/add_NCBI_annotation_track.md) for the detail)

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

## Change/Add color for feature types

Others feature types will be colored by color-hash. If you want to change or add color for feature types, you can modifiy the style in [ColorByTypeDraggable.js](js/View/Track/ColorByTypeDraggable.js#L84-L124) or use [hooks→modify](http://gmod.org/wiki/JBrowse_Configuration_Guide#HTMLFeatures_Configuration_Options) options for customization.

### color for exon

To change or add color for exon features, you can add more `else...if` statment to **ColorByTypeDraggable.js** at [L59-L75](js/View/Track/ColorByTypeDraggable.js#L59-L75) and [L91-L108](js/View/Track/ColorByTypeDraggable.js#L91-L108).

#### Example:

``` shell
// color of exon
if (type == 'mRNA') {
    div.children[i].children[j].style.backgroundColor = '#d7f7c0';
} else if (type == 'tRNA') {
    div.children[i].children[j].style.backgroundColor = '#ef7902';
} else if (type == '[new_featuretype]') {
    div.children[i].children[j].style.backgroundColor = '[Color Hex Color Codes]';
} else {
    div.children[i].children[j].style.backgroundColor = colorHash.hex(concat_subClassName);
}
```

### color for CDS

To change or add color for CDS features, you can add more `else...if` statment to **ColorByTypeDraggable.js** at [L79-L83](js/View/Track/ColorByTypeDraggable.js#L79-L83) and [L110-L114](js/View/Track/ColorByTypeDraggable.js#L110-L114).

#### Example:

```shell
// color of CDS
if (type == 'mRNA') {
    div.children[i].children[j].style.backgroundColor = '#28db25';
} else if (type == '[new_featuretype]') {
    div.children[i].children[j].style.backgroundColor = '[Color Hex Color Codes]';
} else {
    div.children[i].children[j].style.backgroundColor = colorHash.hex(concat_subClassName);
}
```

## Internal Dependencies

- [css/main.css](css/main.css)
    - The custom css for the track styles.
- [jslib/color-hash](jslib/color-hash)
    - Functions for generating color based on the given string. Download from [color-hash](https://github.com/zenozeng/color-hash).
