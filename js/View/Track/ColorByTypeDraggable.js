var draggable = false;
try {
    var m = require('WebApollo/View/Track/DraggableHTMLFeatures');
    var HTMLFeatures = 'WebApollo/View/Track/DraggableHTMLFeatures';
    draggable = true;
} catch (ex) {
    var HTMLFeatures = 'JBrowse/View/Track/HTMLFeatures';
}

// function getCookie(cname) {
//     var name = cname + "=";
//     var ca = document.cookie.split(';');
//     for(var i=0; i<ca.length; i++) {
//        var c = ca[i];
//        while (c.charAt(0)==' ') c = c.substring(1);
//        if(c.indexOf(name) == 0)
//           return c.substring(name.length,c.length);
//     }
//     return "";
// }

//function getCookie(name) {
    //var match = document.cookie.match(RegExp('(?:^|;\\s*)' + name + '=([^;]*)')); return match ? match[1] : null;
 //}

//var browser=getCookie("colorCdsByFrame");



define([
    'dojo/_base/declare',
    HTMLFeatures,
    'JBrowse/Util',
    'plugins/ColorByType/jslib/color-hash/dist/color-hash',
    'JBrowse/Browser',
],
    function (declare,
        HTMLFeatureTrack,
        Util,
        ColorHash,
        draggable) {
        var ColorByType = declare(HTMLFeatureTrack,
            {
                
                _defaultConfig: function () {
                    return Util.deepUpdate(
                        dojo.clone(this.inherited(arguments)),
                        {
                            style: {
                                className: "container-16px",
                                renderClassName: "gray-center-30pct annot",
                                arrowheadClass: "arrowhead",
                                subfeatureClasses: {
                                    UTR: "generic_NCBI-utr",
                                    CDS: "generic_NCBI-cds",
                                    exon: "container-60pct",
                                    stop_codon_read_through: "stop_codon_read_through"
                                },
                                minSubfeatureWidth: 1,
                                centerChildrenVertically: false
                            },
                            hooks: {
                                modify: function (track, feature, div) {
                                    var colorHash = new ColorHash();
                                    var type = feature.get('type'); // get transcript type
                                    var UTRclasses = track.config.style.subfeatureClasses['UTR'];
                                    var CDSclasses = track.config.style.subfeatureClasses['CDS'];
                                    var EXONclasses = track.config.style.subfeatureClasses['exon'];
                                    var STOP_CODENRTclasses = track.config.style.subfeatureClasses['stop_codon_read_through'];
                                    //var id=feature.get('organismId');
                                    //var it=HTMLFeatureTrack.uniqueId; 
                                    var a=feature.get('id');
                                    var b=feature.get('seq_id');
                                    var c=feature.get('parent');
                                    var d=feature.get('subfeatures');
                                    var e=feature.get('uniqueId');
                                    var f=feature.get('seq');
                       
                                    
                                    //console.log(id);
                                    //console.log(it);
                                    console.log(a);
                                    console.log(b);
                                    console.log(c);
                                    console.log(d);
                                    console.log(e);
                                    console.log(f);
                                    
                                    var browser = localStorage.getItem('GenomeBrowser-colorCdsByFrame-10677');
                                    for (var i = 0; i < div.children.length; i++) {
                                        // container
                                        // style of some common transcript type
                                        var ClassName = div.children[i].className;
                                        if (ClassName.includes('subfeature')) {
                                            var concat_ClassName = type.concat(ClassName);
                                            // children of a container
                                            if (div.children[i].children.length > 0) {
                                                for (var j = 0; j < div.children[i].children.length; j++) {
                                                    var subClassName = div.children[i].children[j].className;
                                                    var concat_subClassName = type.concat(subClassName);
                                                    if (typeof UTRclasses !== "undefined" && subClassName.includes(UTRclasses)) {
                                                        // UTR
                                                        // color of exon
                                                        if (type == 'mRNA') {
                                                            div.children[i].children[j].style.backgroundColor = '#d7f7c0';
                                                        } else if (type == 'lnc_RNA') {
                                                            div.children[i].children[j].style.backgroundColor = '#262dff';
                                                        } else if (type == 'snoRNA') {
                                                            div.children[i].children[j].style.backgroundColor = '#7cedff';
                                                        } else if (type == 'transcript') {
                                                            div.children[i].children[j].style.backgroundColor = '#c589c6';
                                                        } else if (type == 'rRNA') {
                                                            div.children[i].children[j].style.backgroundColor = '#fff200';
                                                        } else if (type == 'snRNA') {
                                                            div.children[i].children[j].style.backgroundColor = '#80a823';
                                                        } else if (type == 'tRNA') {
                                                            div.children[i].children[j].style.backgroundColor = '#ef7902';
                                                        } else {
                                                            div.children[i].children[j].style.backgroundColor = colorHash.hex(concat_subClassName);
                                                        }
                                                    } 
                                                    else if (typeof CDSclasses !== "undefined" && subClassName.includes(CDSclasses)) {
                                                        // CDS
                                                        // color of CDS
                                                        console.log(browser)
                                                        if (type == 'mRNA') {
                                                            console.log( "MRNA starting" );
                                                        
                                                            if(browser!=="true"){
                                                            div.children[i].children[j].style.backgroundColor = '#28db25';
                                                            console.log("CBT");}                                                                                                    
                                                        
                                                            else{
                                                            console.log("CDS");
                                                            continue;}   

                                                        } else {
                                                            div.children[i].children[j].style.backgroundColor = colorHash.hex(concat_subClassName);                                                    
                                                        }
                                                    } 
                                                    else {
                                                        // other feature type
                                                        div.children[i].children[j].className = 'subfeature generic_NCBI-utr';
                                                        div.children[i].children[j].style.backgroundColor = colorHash.hex(concat_subClassName);
                                                    }
                                                }
                                            } else {
                                                if ((typeof UTRclasses !== "undefined" && ClassName.includes(UTRclasses)) || (typeof EXONclasses !== "undefined" && ClassName.includes(EXONclasses))) {
                                                    if (type == 'mRNA') {
                                                        div.children[i].style.backgroundColor = '#d7f7c0';
                                                    } else if (type == 'lnc_RNA') {
                                                        div.children[i].style.backgroundColor = '#262dff';
                                                    } else if (type == 'snoRNA') {
                                                        div.children[i].style.backgroundColor = '#7cedff';
                                                    } else if (type == 'transcript') {
                                                        div.children[i].style.backgroundColor = '#c589c6';
                                                    } else if (type == 'rRNA') {
                                                        div.children[i].style.backgroundColor = '#fff200';
                                                    } else if (type == 'snRNA') {
                                                        div.children[i].style.backgroundColor = '#80a823';
                                                    } else if (type == 'tRNA') {
                                                        div.children[i].style.backgroundColor = '#ef7902';
                                                    } else {
                                                        div.children[i].style.backgroundColor = colorHash.hex(concat_ClassName);
                                                    }
                                                } else if (typeof CDSclasses !== "undefined" && ClassName.includes(CDSclasses)) {
                                                    if (type == 'mRNA') {
                                                        
                                                        if(browser!=="true"){
                                                            div.children[i].style.backgroundColor = '#28db25';
                                                            console.log( "CBT" );
                                                        }
                                                        else{
                                                            console.log("CDS")
                                                            continue;
                                                        }
                                                                                                    
                                                    } else {
                                                        div.children[i].style.backgroundColor = colorHash.hex(concat_ClassName);                                                       
                                                    }
                                                } else if (typeof STOP_CODENRTclasses != "undefined" && ClassName.includes(STOP_CODENRTclasses)) {
                                                    div.children[i].className = 'subfeature stop_codon_read_through';
                                                } else {
                                                    div.children[i].className = 'subfeature generic_NCBI-utr';
                                                    div.children[i].style.backgroundColor = colorHash.hex(concat_ClassName);
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    );
                },
                
                renderFeature: function (feature, uniqueId, block, scale, labelScale, descriptionScale, containerStart, containerEnd, rclass, clsName) {
                    if (draggable == true) {
                        var featdiv = HTMLFeatureTrack.prototype.renderFeature.call(this, feature, uniqueId, block, scale, labelScale, descriptionScale, containerStart, containerEnd, rclass, clsName);
                    } else {
                        var featdiv = this.inherited( arguments );
                        if ( featdiv )  {
                            if (!rclass) {
                                rclass = this.config.style.renderClassName;
                            }
                            if (rclass)  {
                                // console.log("in FeatureTrack.renderFeature, creating annot div");
                                var rendiv = document.createElement("div");
                                dojo.addClass(rendiv, "feature-render");
                                dojo.addClass(rendiv, rclass);
                                if (Util.is_ie6) rendiv.appendChild(document.createComment());
                                featdiv.appendChild(rendiv);
                            }
                            if (clsName) {
                                dojo.removeClass(featdiv.firstChild, feature.get("type"));
                                dojo.addClass(featdiv.firstChild, clsName);
                            }
                        }
                    }
                    return featdiv;
                }
            });
        return ColorByType;
    });
