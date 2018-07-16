/* jshint browser: true */
(function(window, document) {/* Wrap code in an IIFE */
/* date last modified: 2017-05-29 12:41:49 */
var jQuery, $; // Localize jQuery variables
var waitForFinalEvent = (function() {
    var timers = {};
    return function(callback, ms, uniqueId) {
        if (!uniqueId) {
            uniqueId = "Don't call this twice without a uniqueId";
        }
        if (timers[uniqueId]) {
            clearTimeout (timers[uniqueId]);
        }
        timers[uniqueId] = setTimeout(callback, ms);
    };
})();

function loadScript(url, callback) {
  /* Load script from url and calls callback once it's loaded */
  var scriptTag = document.createElement('script');
  scriptTag.setAttribute("type", "text/javascript");
  scriptTag.setAttribute("src", url);
  if (typeof callback !== "undefined") {
    if (scriptTag.readyState) {
      /* For old versions of IE */
      scriptTag.onreadystatechange = function () {
        if (this.readyState === 'complete' || this.readyState === 'loaded') {
          callback();
        }
      };
    } else {
      scriptTag.onload = callback;
    }
  }
  (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(scriptTag);
}

var isH = false;

function main() {
  /* The main logic of our widget */

    var script_el = $('#clustrmaps');
    var old_code = false;

    if(script_el.length === 0){
        script_el = $('#clustrmaps-widget');
        old_code = true;
    }

    if( script_el.length !== 1){
        return;
    }
    
    var clusrtmaps_widget;
    var insert_after = true;
    
    if(script_el.parents('head').length !== 0) {
        insert_after = false;   
    }

    function bgUrl(data) {
        var base = '//clustrmaps.com/generated_content/backs/bg';
        var ap = ['w', 'co', 'cl'];
        var p = [];
        for ( var i in ap ) {
           var v = ap[i];
           if ( v in data ) {
              p.push(v + "_" + data[v]);
           }
        }

        if (p.length > 0 ) {
            base += '-' + p.join('-');
        }

        return base + ".png";
    }

    function adjustElements(data) {
        var co = ( 'co' in data ) ? data['co'] : '2d78ad';
        var ct = ( 'ct' in data ) ? data['ct'] : 'ffffff';
        var w = data['w'];
        var h  = w / 2.04;

        $('.clustrmaps-map-container').css ('background-color', '#' + co);
        $('#clustrmaps-widget-v2').addClass('clustrmaps-map-control');

        $('.clustrmaps-map').css ( 'width', w + 'px');
        $('.clustrmaps-map').css ( 'height', h + 'px');
        $('.clustrmaps-map').css ('background-image', 'url("' + bgUrl(data) + '")');

        var uF = 12, dF = 12, lH = 16;

        if ( w >= 600 ) {
             uF = 14;
             dF = 16;
             lH = 22;
        } else if( w >= 400 ) {
             uF = 14;
             dF = 14;
             lH = 22;
        }

        $('.clustrmaps-visitors, .clustrmaps-date').css('font-size', uF + 'px')
                                                   .css('line-height', '16px')
                                                   .css('color', '#' + ct );

        $('.clustrmaps-bottom-text').css('font-size', dF + 'px')
                        .css('line-height', lH + 'px')
                        .css('color', 'white');


        $("<div class=clustrmaps-loading style='display: table; height: 100%; overflow: hidden; width:100%'><div style='font-size: 14px;font-family: \"Helvetica Neue\", Arial; color: white; text-shadow: 1px 1px 0 #01324f; display: table-cell; vertical-align: middle; text-align: center'>Loading data...</div></div>").appendTo($('.clustrmaps-map'));
    }

    function counterCode() {
        
        if ( !embed_clustrmaps(script_el, insert_after) ) {
            return false;
        }

        var data = {};
        var urlParams = {};
        
        if (old_code){
            data = {'old_code': true, 'd': _clustrmaps.url, 'u': _clustrmaps.user};
        } else {
            var src = script_el.attr('src');
            var query = src.substring(src.indexOf('?'));

            var match,
                pl     = /\+/g,  // Regex for replacing addition symbol with a space
                search = /([^&=]+)=?([^&]*)/g,
                decode = function (s) { return decodeURIComponent(s.replace(pl, " ")); },
                query  = query.substring(1);


            while (match = search.exec(query)){
                urlParams[decode(match[1])] = decode(match[2]);
            }
            data = urlParams;
        }


        if ( !('w' in data) || ( data['w'] == 'a' ) ) {
            var pw = $("#clustrmaps-widget-v2").parent().width();

            if ( !pw ) {
                pw = 300;
            }

            if ( data['w'] != 'a')  {
               if ( pw < 180 ) pw = 180;
               if ( pw > 300 ) pw = 300;
            }
            data['w'] = pw;
        }

        if ( !('t' in data) ) {
            data['t'] = 'm';
        }

        if ( data['t'] != 'm' ) {
            $(".clustrmaps-date").hide();
        }

        if ( data['t'] == 'n' ) {
            $(".clustrmaps-visitors").hide();
        }

        if ( 'w' in data ) {
            $("#clustrmaps-widget-v2").css('width', data['w'] + 'px' );
        }

        adjustElements(data);

        if ( isH ) {
            data['hw'] = 1;
        }

        //-- bg-affect here ---
        $.ajax({
            dataType: 'jsonp',
            cache: false,
            data: data,
            url: "//clustrmaps.com/widget_call_home.js",
            success: function(data){
                eval(data);
            }
        });
    }
    
    if ( insert_after ) {
        counterCode();
    } else {
        $(function() {
            counterCode();
        });
    }

}//end main()

function embed_clustrmaps(script_el, embed_after_script){

    if($('#clustrmaps-widget-v2').length === 0){

        /*
        if ( script_el.parents(":hidden").length > 0 ) {
            isH = true;
        }
        */
                            var link = '<a target="_top" href="https://clustrmaps.com/?utm_source=widget&utm_medium=js_widget&utm_campaign=widget_ctr" id="clustrmaps-widget-v2">';
        
        var container = $(link
        +'<div class="clustrmaps-map-container">'
        +'<div class="clstm clustrmaps-visitors">&nbsp;</div>'
        +'<div class="clstm clustrmaps-date">&nbsp;</div>'
        +'<div class="clustrmaps-map"></div>'
        //+'<div class="clustrmaps-logo"></div>'
        //+'<div class="clustrmaps-connection"></div>'
        +'</div>'
        //+'<div class="clstm clustrmaps-bottom-text">Click to see details</div>'
        //+'<div class="clstm clustrmaps-bottom-text variation">Click to Enlarge Map</div>'
        +'<div class=""></div>'
        +'</a>');

        if(embed_after_script){
            container.insertAfter(script_el);         
        }else{
            container.appendTo($('body'));   
        }
            


$('#clustrmaps-widget-v2').after('<style type="text/css">a#clustrmaps-widget-v2, #clustrmaps-widget-v2 {    display: block;    font-size: 11px;    line-height: 13px;    margin: 0 auto;    padding: 0;    position: relative;    text-align: center;    color: transparent;    min-height: 139px;    text-decoration: none;    /* text-shadow: 1px 1px 0 #01324f; */    border: 0 none;}.clustrmaps-map {    position: relative;}#clustrmaps-widget-v2 > .clustrmaps-map-container {    background-position: 0 0;    background-repeat: no-repeat;    position: relative;}#clustrmaps-widget-v2 > .clustrmaps-map-container > .clustrmaps-date {    text-align: center;    width: 100%;    z-index: 10;}#clustrmaps-widget-v2 > .clustrmaps-map-container > .clustrmaps-logo {    position: absolute;    background-image: url("//cdn.clustrmaps.com/assets/clustrmaps/img/logo4-small.png");    bottom: 0px;    background-repeat: no-repeat;    background-position: center center;    z-index: 1;    width: 100px;    height: 31px;    left: 0px;}#clustrmaps-widget-v2 > .clustrmaps-map-container > .clustrmaps-connection {    background-position: center center;    background-repeat: no-repeat;    bottom: 0;    color: rgba(255, 255, 255, 0.5);    padding: 4px 4px;    position: absolute;    right: 0;    z-index: 1;    font-variant: small-caps;}#clustrmaps-widget-v2 > .clustrmaps-bottom-text {    letter-spacing: 0px;    background: #FFFFFF;    color: #000000;    text-shadow: none;}#clustrmaps-widget-v2 > .clustrmaps-cursor-click {    background-position: center center;    background-repeat: no-repeat;    display: block;    height: 29px;    position: absolute;    right: 0;    top: 56px;    width: 30px;}#clustrmaps-widget-v2 > .clustrmaps-map-container > .clustrmaps-connection.clustrmaps-failed {    color: rgba(255, 0, 0, 0.8);}/*#clustrmaps-widget-v2 > .clustrmaps-map-container {    background-image: url("//cdn.clustrmaps.com/images/map_v2_loading.png");}*/#clustrmaps-widget-v2 > .clustrmaps-cursor-click {    background-image: url("//cdn.clustrmaps.com/assets/clustrmaps/img/cursor_click.png");}#clustrmaps-widget-v2 > .clustrmaps-bottom-text.variation {    display: none;}/* CONTROL *//*#clustrmaps-widget-v2.clustrmaps-map-control > .clustrmaps-map-container {    background-image: url("//cdn.clustrmaps.com/images/map_v2-control.png");}*/#clustrmaps-widget-v2.clustrmaps-map-control > .clustrmaps-bottom-text {    -webkit-border-radius: 3px;    -moz-border-radius: 3px;    border-radius: 3px;    border: 1px solid #999;    background: #F24D58;    background: -moz-linear-gradient(top, #FF636D 50%, #DD2929 50%);    background: -webkit-gradient(linear, left top, left bottom, color-stop(50%,#f83737), color-stop(50%,#f83737));    background: linear-gradient(to bottom, #FF636D 50%,#DD2929 51%);    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr="#FF636D", endColorstr="#f83737",GradientType=0 );    display: block;    margin: 2px auto 0;    padding: 3px 14px;    color: #FFFFFF;    text-shadow: 1px 1px 0px #5B0000;    font-weight: 600;}#clustrmaps-widget-v2.clustrmaps-map-control  > .clustrmaps-bottom-text:hover {    border: 1px solid #888;    background: #a3f5a2;    background: -moz-linear-gradient(top,  #ed8b92 50%, #D76666 50%);    background: -webkit-gradient(linear, left top, left bottom, color-stop(50%,#ed8b92), color-stop(50%,#D76666));    background: linear-gradient(to bottom, #ed8b92 50%,#D76666 51%);    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr="#ed8b92", endColorstr="#D76666",GradientType=0 );}#clustrmaps-widget-v2.clustrmaps-map-control > .clustrmaps-bottom-text.variation {    display: none;}.clstm {    text-transform: capitalize !important;    position: relative;}#clustrmaps-widget-v2.clustrmaps-map-variation > .clustrmaps-bottom-text {    -webkit-border-radius: 3px;    -moz-border-radius: 3px;    border-radius: 3px;    border: 1px solid #999;    background: #F24D58;    background: -moz-linear-gradient(top, #FF636D 50%, #DD2929 50%);    background: -webkit-gradient(linear, left top, left bottom, color-stop(50%,#f83737), color-stop(50%,#f83737));    background: linear-gradient(to bottom, #FF636D 50%,#DD2929 51%);    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr="#FF636D", endColorstr="#f83737",GradientType=0 );    display: block;    margin: 2px auto 0;    padding: 3px 14px;    color: #FFFFFF;    text-shadow: 1px 1px 0px #5B0000;    font-weight: 600;}#clustrmaps-widget-v2.clustrmaps-map-variation > .clustrmaps-bottom-text {    display: none;}#clustrmaps-widget-v2.clustrmaps-map-variation > .clustrmaps-bottom-text.variation {    display: block;}#clustrmaps-widget-v2.clustrmaps-map-variation  > .clustrmaps-bottom-text:hover {    border: 1px solid #888;    background: #a3f5a2;    background: -moz-linear-gradient(top,  #ed8b92 50%, #D76666 50%);    background: -webkit-gradient(linear, left top, left bottom, color-stop(50%,#ed8b92), color-stop(50%,#D76666));    background: linear-gradient(to bottom, #ed8b92 50%,#D76666 51%);    filter: progid:DXImageTransform.Microsoft.gradient( startColorstr="#ed8b92", endColorstr="#D76666",GradientType=0 );}.clustrmaps-visitors, .clustrmaps-date, .clustrmaps-bottom-text {    font-family: Arial, Helvetica, sans-serif;    text-align: center;    font-weight: normal;}.clustrmaps-bottom-text {    font-size: 12px;}</style>');
$('#clustrmaps-widget-v2').after('<style type="text/css">.jvectormap-container {    width: 100%;    height: 100%;    position: absolute;    overflow: hidden;}.jvectormap-tip {    position: absolute;    display: none;    border: solid 1px #CDCDCD;    border-radius: 3px;    background: #292929;    color: white;    font-family: Arial, Helvetica, sans-serif;    padding: 3px;    z-index: 9999;    font-size: 11px;    line-height: 13px;}.jvectormap-zoomin, .jvectormap-zoomout, .jvectormap-goback {    background: #ffffff none repeat scroll 0 0;    border: 1px solid #bebebe;    border-radius: 2px;    box-sizing: content-box;    color: #838383;    cursor: pointer;    font-weight: bold;    left: 10px;    padding: 3px;    position: absolute;    text-align: center;    z-index: 1;}.jvectormap-zoomin, .jvectormap-zoomout {    padding: 2px 10px;}.jvectormap-zoomin {    top: 10px;}.jvectormap-zoomout {    top: 37px;}.jvectormap-goback {    bottom: 10px;    z-index: 1000;    padding: 6px;}.jvectormap-spinner {    position: absolute;    left: 0;    top: 0;    right: 0;    bottom: 0;    background: center no-repeat url(data:image/gif;base64,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);}.jvectormap-legend-title {    font-weight: bold;    font-size: 14px;    text-align: center;}.jvectormap-legend-cnt {    position: absolute;}.jvectormap-legend-cnt-h {    bottom: 0;    right: 0;}.jvectormap-legend-cnt-v {    top: 0;    right: 0;}.jvectormap-legend {    background: black;    color: white;    border-radius: 3px;}.jvectormap-legend-cnt-h .jvectormap-legend {    float: left;    margin: 0 10px 10px 0;    padding: 3px 3px 1px 3px;}.jvectormap-legend-cnt-h .jvectormap-legend .jvectormap-legend-tick {    float: left;}.jvectormap-legend-cnt-v .jvectormap-legend {    margin: 10px 10px 0 0;    padding: 3px;}.jvectormap-legend-cnt-h .jvectormap-legend-tick {    width: 40px;}.jvectormap-legend-cnt-h .jvectormap-legend-tick-sample {    height: 15px;}.jvectormap-legend-cnt-v .jvectormap-legend-tick-sample {    height: 20px;    width: 20px;    display: inline-block;    vertical-align: middle;}.jvectormap-legend-tick-text {    font-size: 12px;}.jvectormap-legend-cnt-h .jvectormap-legend-tick-text {    text-align: center;}.jvectormap-legend-cnt-v .jvectormap-legend-tick-text {    display: inline-block;    vertical-align: middle;    line-height: 20px;    padding-left: 3px;}</style>');                            
        return true;                     
    }
    
    return false;
}


function loadLibs() {
                        !function(t){var e={set:{colors:1,values:1,backgroundColor:1,scaleColors:1,normalizeFunction:1,focus:1},get:{selectedRegions:1,selectedMarkers:1,mapObject:1,regionName:1}};t.fn.vectorMap=function(t){var a,s,a=this.children(".jvectormap-container").data("mapObject");if("addMap"===t)jvm.Map.maps[arguments[1]]=arguments[2];else{if(("set"===t||"get"===t)&&e[t][arguments[1]])return s=arguments[1].charAt(0).toUpperCase()+arguments[1].substr(1),a[t+s].apply(a,Array.prototype.slice.call(arguments,2));t=t||{},t.container=this,a=new jvm.Map(t)}return this}}(jQuery),function(t){"function"==typeof define&&define.amd?define(["jquery"],t):"object"==typeof exports?module.exports=t:t(jQuery)}(function(t){function e(e){var r=e||window.event,o=h.call(arguments,1),l=0,m=0,c=0,p=0;if(e=t.event.fix(r),e.type="mousewheel","detail"in r&&(c=-1*r.detail),"wheelDelta"in r&&(c=r.wheelDelta),"wheelDeltaY"in r&&(c=r.wheelDeltaY),"wheelDeltaX"in r&&(m=-1*r.wheelDeltaX),"axis"in r&&r.axis===r.HORIZONTAL_AXIS&&(m=-1*c,c=0),l=0===c?m:c,"deltaY"in r&&(c=-1*r.deltaY,l=c),"deltaX"in r&&(m=r.deltaX,0===c&&(l=-1*m)),0!==c||0!==m){if(1===r.deltaMode){var d=t.data(this,"mousewheel-line-height");l*=d,c*=d,m*=d}else if(2===r.deltaMode){var u=t.data(this,"mousewheel-page-height");l*=u,c*=u,m*=u}return p=Math.max(Math.abs(c),Math.abs(m)),(!n||n>p)&&(n=p,s(r,p)&&(n/=40)),s(r,p)&&(l/=40,m/=40,c/=40),l=Math[l>=1?"floor":"ceil"](l/n),m=Math[m>=1?"floor":"ceil"](m/n),c=Math[c>=1?"floor":"ceil"](c/n),e.deltaX=m,e.deltaY=c,e.deltaFactor=n,e.deltaMode=0,o.unshift(e,l,m,c),i&&clearTimeout(i),i=setTimeout(a,200),(t.event.dispatch||t.event.handle).apply(this,o)}}function a(){n=null}function s(t,e){return m.settings.adjustOldDeltas&&"mousewheel"===t.type&&e%120===0}var i,n,r=["wheel","mousewheel","DOMMouseScroll","MozMousePixelScroll"],o="onwheel"in document||document.documentMode>=9?["wheel"]:["mousewheel","DomMouseScroll","MozMousePixelScroll"],h=Array.prototype.slice;if(t.event.fixHooks)for(var l=r.length;l;)t.event.fixHooks[r[--l]]=t.event.mouseHooks;var m=t.event.special.mousewheel={version:"3.1.9",setup:function(){if(this.addEventListener)for(var a=o.length;a;)this.addEventListener(o[--a],e,!1);else this.onmousewheel=e;t.data(this,"mousewheel-line-height",m.getLineHeight(this)),t.data(this,"mousewheel-page-height",m.getPageHeight(this))},teardown:function(){if(this.removeEventListener)for(var t=o.length;t;)this.removeEventListener(o[--t],e,!1);else this.onmousewheel=null},getLineHeight:function(e){return parseInt(t(e)["offsetParent"in t.fn?"offsetParent":"parent"]().css("fontSize"),10)},getPageHeight:function(e){return t(e).height()},settings:{adjustOldDeltas:!0}};t.fn.extend({mousewheel:function(t){return t?this.bind("mousewheel",t):this.trigger("mousewheel")},unmousewheel:function(t){return this.unbind("mousewheel",t)}})});var jvm={inherits:function(t,e){function a(){}a.prototype=e.prototype,t.prototype=new a,t.prototype.constructor=t,t.parentClass=e},mixin:function(t,e){var a;for(a in e.prototype)e.prototype.hasOwnProperty(a)&&(t.prototype[a]=e.prototype[a])},min:function(t){var e,a=Number.MAX_VALUE;if(t instanceof Array)for(e=0;e<t.length;e++)t[e]<a&&(a=t[e]);else for(e in t)t[e]<a&&(a=t[e]);return a},max:function(t){var e,a=Number.MIN_VALUE;if(t instanceof Array)for(e=0;e<t.length;e++)t[e]>a&&(a=t[e]);else for(e in t)t[e]>a&&(a=t[e]);return a},keys:function(t){var e,a=[];for(e in t)a.push(e);return a},values:function(t){var e,a,s=[];for(a=0;a<arguments.length;a++){t=arguments[a];for(e in t)s.push(t[e])}return s},whenImageLoaded:function(t){var e=new jvm.$.Deferred,a=jvm.$("<img/>");return a.error(function(){e.reject()}).load(function(){e.resolve(a)}),a.attr("src",t),e},isImageUrl:function(t){return/\.\w{3,4}$/.test(t)}};jvm.$=jQuery,Array.prototype.indexOf||(Array.prototype.indexOf=function(t,e){var a;if(null==this)throw new TypeError('"this" is null or not defined');var s=Object(this),i=s.length>>>0;if(0===i)return-1;var n=+e||0;if(Math.abs(n)===1/0&&(n=0),n>=i)return-1;for(a=Math.max(n>=0?n:i-Math.abs(n),0);i>a;){if(a in s&&s[a]===t)return a;a++}return-1}),jvm.AbstractElement=function(t,e){this.node=this.createElement(t),this.name=t,this.properties={},e&&this.set(e)},jvm.AbstractElement.prototype.set=function(t,e){var a;if("object"==typeof t)for(a in t)this.properties[a]=t[a],this.applyAttr(a,t[a]);else this.properties[t]=e,this.applyAttr(t,e)},jvm.AbstractElement.prototype.get=function(t){return this.properties[t]},jvm.AbstractElement.prototype.applyAttr=function(t,e){this.node.setAttribute(t,e)},jvm.AbstractElement.prototype.remove=function(){jvm.$(this.node).remove()},jvm.AbstractCanvasElement=function(t,e,a){this.container=t,this.setSize(e,a),this.rootElement=new jvm[this.classPrefix+"GroupElement"],this.node.appendChild(this.rootElement.node),this.container.appendChild(this.node)},jvm.AbstractCanvasElement.prototype.add=function(t,e){e=e||this.rootElement,e.add(t),t.canvas=this},jvm.AbstractCanvasElement.prototype.addPath=function(t,e,a){var s=new jvm[this.classPrefix+"PathElement"](t,e);return this.add(s,a),s},jvm.AbstractCanvasElement.prototype.addCircle=function(t,e,a){var s=new jvm[this.classPrefix+"CircleElement"](t,e);return this.add(s,a),s},jvm.AbstractCanvasElement.prototype.addImage=function(t,e,a){var s=new jvm[this.classPrefix+"ImageElement"](t,e);return this.add(s,a),s},jvm.AbstractCanvasElement.prototype.addText=function(t,e,a){var s=new jvm[this.classPrefix+"TextElement"](t,e);return this.add(s,a),s},jvm.AbstractCanvasElement.prototype.addGroup=function(t){var e=new jvm[this.classPrefix+"GroupElement"];return t?t.node.appendChild(e.node):this.node.appendChild(e.node),e.canvas=this,e},jvm.AbstractShapeElement=function(t,e,a){this.style=a||{},this.style.current=this.style.current||{},this.isHovered=!1,this.isSelected=!1,this.updateStyle()},jvm.AbstractShapeElement.prototype.setStyle=function(t,e){var a={};"object"==typeof t?a=t:a[t]=e,jvm.$.extend(this.style.current,a),this.updateStyle()},jvm.AbstractShapeElement.prototype.updateStyle=function(){var t={};jvm.AbstractShapeElement.mergeStyles(t,this.style.initial),jvm.AbstractShapeElement.mergeStyles(t,this.style.current),this.isHovered&&jvm.AbstractShapeElement.mergeStyles(t,this.style.hover),this.isSelected&&(jvm.AbstractShapeElement.mergeStyles(t,this.style.selected),this.isHovered&&jvm.AbstractShapeElement.mergeStyles(t,this.style.selectedHover)),this.set(t)},jvm.AbstractShapeElement.mergeStyles=function(t,e){var a;e=e||{};for(a in e)null===e[a]?delete t[a]:t[a]=e[a]},jvm.SVGElement=function(t,e){jvm.SVGElement.parentClass.apply(this,arguments)},jvm.inherits(jvm.SVGElement,jvm.AbstractElement),jvm.SVGElement.svgns="http://www.w3.org/2000/svg",jvm.SVGElement.prototype.createElement=function(t){return document.createElementNS(jvm.SVGElement.svgns,t)},jvm.SVGElement.prototype.addClass=function(t){this.node.setAttribute("class",t)},jvm.SVGElement.prototype.getElementCtr=function(t){return jvm["SVG"+t]},jvm.SVGElement.prototype.getBBox=function(){return this.node.getBBox()},jvm.SVGGroupElement=function(){jvm.SVGGroupElement.parentClass.call(this,"g")},jvm.inherits(jvm.SVGGroupElement,jvm.SVGElement),jvm.SVGGroupElement.prototype.add=function(t){this.node.appendChild(t.node)},jvm.SVGCanvasElement=function(t,e,a){this.classPrefix="SVG",jvm.SVGCanvasElement.parentClass.call(this,"svg"),this.defsElement=new jvm.SVGElement("defs"),this.node.appendChild(this.defsElement.node),jvm.AbstractCanvasElement.apply(this,arguments)},jvm.inherits(jvm.SVGCanvasElement,jvm.SVGElement),jvm.mixin(jvm.SVGCanvasElement,jvm.AbstractCanvasElement),jvm.SVGCanvasElement.prototype.setSize=function(t,e){this.width=t,this.height=e,this.node.setAttribute("width",t),this.node.setAttribute("height",e)},jvm.SVGCanvasElement.prototype.applyTransformParams=function(t,e,a){this.scale=t,this.transX=e,this.transY=a,this.rootElement.node.setAttribute("transform","scale("+t+") translate("+e+", "+a+")")},jvm.SVGShapeElement=function(t,e,a){jvm.SVGShapeElement.parentClass.call(this,t,e),jvm.AbstractShapeElement.apply(this,arguments)},jvm.inherits(jvm.SVGShapeElement,jvm.SVGElement),jvm.mixin(jvm.SVGShapeElement,jvm.AbstractShapeElement),jvm.SVGShapeElement.prototype.applyAttr=function(t,e){var a,s,i=this;"fill"===t&&jvm.isImageUrl(e)?jvm.SVGShapeElement.images[e]?this.applyAttr("fill","url(#image"+jvm.SVGShapeElement.images[e]+")"):jvm.whenImageLoaded(e).then(function(t){s=new jvm.SVGElement("image"),s.node.setAttributeNS("http://www.w3.org/1999/xlink","href",e),s.applyAttr("x","0"),s.applyAttr("y","0"),s.applyAttr("width",t[0].width),s.applyAttr("height",t[0].height),a=new jvm.SVGElement("pattern"),a.applyAttr("id","image"+jvm.SVGShapeElement.imageCounter),a.applyAttr("x",0),a.applyAttr("y",0),a.applyAttr("width",t[0].width/2),a.applyAttr("height",t[0].height/2),a.applyAttr("viewBox","0 0 "+t[0].width+" "+t[0].height),a.applyAttr("patternUnits","userSpaceOnUse"),a.node.appendChild(s.node),i.canvas.defsElement.node.appendChild(a.node),jvm.SVGShapeElement.images[e]=jvm.SVGShapeElement.imageCounter++,i.applyAttr("fill","url(#image"+jvm.SVGShapeElement.images[e]+")")}):jvm.SVGShapeElement.parentClass.prototype.applyAttr.apply(this,arguments)},jvm.SVGShapeElement.imageCounter=1,jvm.SVGShapeElement.images={},jvm.SVGPathElement=function(t,e){jvm.SVGPathElement.parentClass.call(this,"path",t,e),this.node.setAttribute("fill-rule","evenodd")},jvm.inherits(jvm.SVGPathElement,jvm.SVGShapeElement),jvm.SVGCircleElement=function(t,e){jvm.SVGCircleElement.parentClass.call(this,"circle",t,e)},jvm.inherits(jvm.SVGCircleElement,jvm.SVGShapeElement),jvm.SVGImageElement=function(t,e){jvm.SVGImageElement.parentClass.call(this,"image",t,e)},jvm.inherits(jvm.SVGImageElement,jvm.SVGShapeElement),jvm.SVGImageElement.prototype.applyAttr=function(t,e){var a=this;"image"==t?jvm.whenImageLoaded(e).then(function(t){a.node.setAttributeNS("http://www.w3.org/1999/xlink","href",e),a.width=t[0].width,a.height=t[0].height,a.applyAttr("width",a.width),a.applyAttr("height",a.height),a.applyAttr("x",a.cx-a.width/2),a.applyAttr("y",a.cy-a.height/2),jvm.$(a.node).trigger("imageloaded",[t])}):"cx"==t?(this.cx=e,this.width&&this.applyAttr("x",e-this.width/2)):"cy"==t?(this.cy=e,this.height&&this.applyAttr("y",e-this.height/2)):jvm.SVGImageElement.parentClass.prototype.applyAttr.apply(this,arguments)},jvm.SVGTextElement=function(t,e){jvm.SVGTextElement.parentClass.call(this,"text",t,e)},jvm.inherits(jvm.SVGTextElement,jvm.SVGShapeElement),jvm.SVGTextElement.prototype.applyAttr=function(t,e){"text"===t?this.node.textContent=e:jvm.SVGTextElement.parentClass.prototype.applyAttr.apply(this,arguments)},jvm.VMLElement=function(t,e){jvm.VMLElement.VMLInitialized||jvm.VMLElement.initializeVML(),jvm.VMLElement.parentClass.apply(this,arguments)},jvm.inherits(jvm.VMLElement,jvm.AbstractElement),jvm.VMLElement.VMLInitialized=!1,jvm.VMLElement.initializeVML=function(){try{document.namespaces.rvml||document.namespaces.add("rvml","urn:schemas-microsoft-com:vml"),jvm.VMLElement.prototype.createElement=function(t){return document.createElement("<rvml:"+t+' class="rvml">')}}catch(t){jvm.VMLElement.prototype.createElement=function(t){return document.createElement("<"+t+' xmlns="urn:schemas-microsoft.com:vml" class="rvml">')}}document.createStyleSheet().addRule(".rvml","behavior:url(#default#VML)"),jvm.VMLElement.VMLInitialized=!0},jvm.VMLElement.prototype.getElementCtr=function(t){return jvm["VML"+t]},jvm.VMLElement.prototype.addClass=function(t){jvm.$(this.node).addClass(t)},jvm.VMLElement.prototype.applyAttr=function(t,e){this.node[t]=e},jvm.VMLElement.prototype.getBBox=function(){var t=jvm.$(this.node);return{x:t.position().left/this.canvas.scale,y:t.position().top/this.canvas.scale,width:t.width()/this.canvas.scale,height:t.height()/this.canvas.scale}},jvm.VMLGroupElement=function(){jvm.VMLGroupElement.parentClass.call(this,"group"),this.node.style.left="0px",this.node.style.top="0px",this.node.coordorigin="0 0"},jvm.inherits(jvm.VMLGroupElement,jvm.VMLElement),jvm.VMLGroupElement.prototype.add=function(t){this.node.appendChild(t.node)},jvm.VMLCanvasElement=function(t,e,a){this.classPrefix="VML",jvm.VMLCanvasElement.parentClass.call(this,"group"),jvm.AbstractCanvasElement.apply(this,arguments),this.node.style.position="absolute"},jvm.inherits(jvm.VMLCanvasElement,jvm.VMLElement),jvm.mixin(jvm.VMLCanvasElement,jvm.AbstractCanvasElement),jvm.VMLCanvasElement.prototype.setSize=function(t,e){var a,s,i,n;if(this.width=t,this.height=e,this.node.style.width=t+"px",this.node.style.height=e+"px",this.node.coordsize=t+" "+e,this.node.coordorigin="0 0",this.rootElement){for(a=this.rootElement.node.getElementsByTagName("shape"),i=0,n=a.length;n>i;i++)a[i].coordsize=t+" "+e,a[i].style.width=t+"px",a[i].style.height=e+"px";for(s=this.node.getElementsByTagName("group"),i=0,n=s.length;n>i;i++)s[i].coordsize=t+" "+e,s[i].style.width=t+"px",s[i].style.height=e+"px"}},jvm.VMLCanvasElement.prototype.applyTransformParams=function(t,e,a){this.scale=t,this.transX=e,this.transY=a,this.rootElement.node.coordorigin=this.width-e-this.width/100+","+(this.height-a-this.height/100),this.rootElement.node.coordsize=this.width/t+","+this.height/t},jvm.VMLShapeElement=function(t,e){jvm.VMLShapeElement.parentClass.call(this,t,e),this.fillElement=new jvm.VMLElement("fill"),this.strokeElement=new jvm.VMLElement("stroke"),this.node.appendChild(this.fillElement.node),this.node.appendChild(this.strokeElement.node),this.node.stroked=!1,jvm.AbstractShapeElement.apply(this,arguments)},jvm.inherits(jvm.VMLShapeElement,jvm.VMLElement),jvm.mixin(jvm.VMLShapeElement,jvm.AbstractShapeElement),jvm.VMLShapeElement.prototype.applyAttr=function(t,e){switch(t){case"fill":this.node.fillcolor=e;break;case"fill-opacity":this.fillElement.node.opacity=Math.round(100*e)+"%";break;case"stroke":"none"===e?this.node.stroked=!1:this.node.stroked=!0,this.node.strokecolor=e;break;case"stroke-opacity":this.strokeElement.node.opacity=Math.round(100*e)+"%";break;case"stroke-width":0===parseInt(e,10)?this.node.stroked=!1:this.node.stroked=!0,this.node.strokeweight=e;break;case"d":this.node.path=jvm.VMLPathElement.pathSvgToVml(e);break;default:jvm.VMLShapeElement.parentClass.prototype.applyAttr.apply(this,arguments)}},jvm.VMLPathElement=function(t,e){var a=new jvm.VMLElement("skew");jvm.VMLPathElement.parentClass.call(this,"shape",t,e),this.node.coordorigin="0 0",a.node.on=!0,a.node.matrix="0.01,0,0,0.01,0,0",a.node.offset="0,0",this.node.appendChild(a.node)},jvm.inherits(jvm.VMLPathElement,jvm.VMLShapeElement),jvm.VMLPathElement.prototype.applyAttr=function(t,e){"d"===t?this.node.path=jvm.VMLPathElement.pathSvgToVml(e):jvm.VMLShapeElement.prototype.applyAttr.call(this,t,e)},jvm.VMLPathElement.pathSvgToVml=function(t){var e,a,s=0,i=0;return t=t.replace(/(-?\d+)e(-?\d+)/g,"0"),t.replace(/([MmLlHhVvCcSs])\s*((?:-?\d*(?:\.\d+)?\s*,?\s*)+)/g,function(t,n,r,o){r=r.replace(/(\d)-/g,"$1,-").replace(/^\s+/g,"").replace(/\s+$/g,"").replace(/\s+/g,",").split(","),r[0]||r.shift();for(var h=0,l=r.length;l>h;h++)r[h]=Math.round(100*r[h]);switch(n){case"m":return s+=r[0],i+=r[1],"t"+r.join(",");case"M":return s=r[0],i=r[1],"m"+r.join(",");case"l":return s+=r[0],i+=r[1],"r"+r.join(",");case"L":return s=r[0],i=r[1],"l"+r.join(",");case"h":return s+=r[0],"r"+r[0]+",0";case"H":return s=r[0],"l"+s+","+i;case"v":return i+=r[0],"r0,"+r[0];case"V":return i=r[0],"l"+s+","+i;case"c":return e=s+r[r.length-4],a=i+r[r.length-3],s+=r[r.length-2],i+=r[r.length-1],"v"+r.join(",");case"C":return e=r[r.length-4],a=r[r.length-3],s=r[r.length-2],i=r[r.length-1],"c"+r.join(",");case"s":return r.unshift(i-a),r.unshift(s-e),e=s+r[r.length-4],a=i+r[r.length-3],s+=r[r.length-2],i+=r[r.length-1],"v"+r.join(",");case"S":return r.unshift(i+i-a),r.unshift(s+s-e),e=r[r.length-4],a=r[r.length-3],s=r[r.length-2],i=r[r.length-1],"c"+r.join(",")}return""}).replace(/z/g,"e")},jvm.VMLCircleElement=function(t,e){jvm.VMLCircleElement.parentClass.call(this,"oval",t,e)},jvm.inherits(jvm.VMLCircleElement,jvm.VMLShapeElement),jvm.VMLCircleElement.prototype.applyAttr=function(t,e){switch(t){case"r":this.node.style.width=2*e+"px",this.node.style.height=2*e+"px",this.applyAttr("cx",this.get("cx")||0),this.applyAttr("cy",this.get("cy")||0);break;case"cx":if(!e)return;this.node.style.left=e-(this.get("r")||0)+"px";break;case"cy":if(!e)return;this.node.style.top=e-(this.get("r")||0)+"px";break;default:jvm.VMLCircleElement.parentClass.prototype.applyAttr.call(this,t,e)}},jvm.VectorCanvas=function(t,e,a){return this.mode=window.SVGAngle?"svg":"vml","svg"==this.mode?this.impl=new jvm.SVGCanvasElement(t,e,a):this.impl=new jvm.VMLCanvasElement(t,e,a),this.impl.mode=this.mode,this.impl},jvm.SimpleScale=function(t){this.scale=t},jvm.SimpleScale.prototype.getValue=function(t){return t},jvm.OrdinalScale=function(t){this.scale=t},jvm.OrdinalScale.prototype.getValue=function(t){return this.scale[t]},jvm.OrdinalScale.prototype.getTicks=function(){var t,e=[];for(t in this.scale)e.push({label:t,value:this.scale[t]});return e},jvm.NumericScale=function(t,e,a,s){this.scale=[],e=e||"linear",t&&this.setScale(t),e&&this.setNormalizeFunction(e),"undefined"!=typeof a&&this.setMin(a),"undefined"!=typeof s&&this.setMax(s)},jvm.NumericScale.prototype={setMin:function(t){this.clearMinValue=t,"function"==typeof this.normalize?this.minValue=this.normalize(t):this.minValue=t},setMax:function(t){this.clearMaxValue=t,"function"==typeof this.normalize?this.maxValue=this.normalize(t):this.maxValue=t},setScale:function(t){var e;for(this.scale=[],e=0;e<t.length;e++)this.scale[e]=[t[e]]},setNormalizeFunction:function(t){"polynomial"===t?this.normalize=function(t){return Math.pow(t,.2)}:"linear"===t?delete this.normalize:this.normalize=t,this.setMin(this.clearMinValue),this.setMax(this.clearMaxValue)},getValue:function(t){var e,a,s=[],i=0,n=0;for("function"==typeof this.normalize&&(t=this.normalize(t)),n=0;n<this.scale.length-1;n++)e=this.vectorLength(this.vectorSubtract(this.scale[n+1],this.scale[n])),s.push(e),i+=e;for(a=(this.maxValue-this.minValue)/i,n=0;n<s.length;n++)s[n]*=a;for(n=0,t-=this.minValue;t-s[n]>=0;)t-=s[n],n++;return t=this.vectorToNum(n==this.scale.length-1?this.scale[n]:this.vectorAdd(this.scale[n],this.vectorMult(this.vectorSubtract(this.scale[n+1],this.scale[n]),t/s[n])))},vectorToNum:function(t){var e,a=0;for(e=0;e<t.length;e++)a+=Math.round(t[e])*Math.pow(256,t.length-e-1);return a},vectorSubtract:function(t,e){var a,s=[];for(a=0;a<t.length;a++)s[a]=t[a]-e[a];return s},vectorAdd:function(t,e){var a,s=[];for(a=0;a<t.length;a++)s[a]=t[a]+e[a];return s},vectorMult:function(t,e){var a,s=[];for(a=0;a<t.length;a++)s[a]=t[a]*e;return s},vectorLength:function(t){var e,a=0;for(e=0;e<t.length;e++)a+=t[e]*t[e];return Math.sqrt(a)},getTicks:function(){var t,e,a=5,s=[this.clearMinValue,this.clearMaxValue],i=s[1]-s[0],n=Math.pow(10,Math.floor(Math.log(i/a)/Math.LN10)),r=a/i*n,o=[];for(.15>=r?n*=10:.35>=r?n*=5:.75>=r&&(n*=2),s[0]=Math.floor(s[0]/n)*n,s[1]=Math.ceil(s[1]/n)*n,t=s[0];t<=s[1];)e=t==s[0]?this.clearMinValue:t==s[1]?this.clearMaxValue:t,o.push({label:t,value:this.getValue(e)}),t+=n;return o}},jvm.ColorScale=function(t,e,a,s){jvm.ColorScale.parentClass.apply(this,arguments)},jvm.inherits(jvm.ColorScale,jvm.NumericScale),jvm.ColorScale.prototype.setScale=function(t){var e;for(e=0;e<t.length;e++)this.scale[e]=jvm.ColorScale.rgbToArray(t[e])},jvm.ColorScale.prototype.getValue=function(t){return jvm.ColorScale.numToRgb(jvm.ColorScale.parentClass.prototype.getValue.call(this,t))},jvm.ColorScale.arrayToRgb=function(t){var e,a,s="#";for(a=0;a<t.length;a++)e=t[a].toString(16),s+=1==e.length?"0"+e:e;return s},jvm.ColorScale.numToRgb=function(t){for(t=t.toString(16);t.length<6;)t="0"+t;return"#"+t},jvm.ColorScale.rgbToArray=function(t){return t=t.substr(1),[parseInt(t.substr(0,2),16),parseInt(t.substr(2,2),16),parseInt(t.substr(4,2),16)]},jvm.Legend=function(t){this.params=t||{},this.map=this.params.map,this.series=this.params.series,this.body=jvm.$("<div/>"),this.body.addClass("jvectormap-legend"),this.params.cssClass&&this.body.addClass(this.params.cssClass),t.vertical?this.map.legendCntVertical.append(this.body):this.map.legendCntHorizontal.append(this.body),this.render()},jvm.Legend.prototype.render=function(){var t,e,a,s,i=this.series.scale.getTicks(),n=jvm.$("<div/>").addClass("jvectormap-legend-inner");for(this.body.html(""),this.params.title&&this.body.append(jvm.$("<div/>").addClass("jvectormap-legend-title").html(this.params.title)),this.body.append(n),t=0;t<i.length;t++){switch(e=jvm.$("<div/>").addClass("jvectormap-legend-tick"),a=jvm.$("<div/>").addClass("jvectormap-legend-tick-sample"),this.series.params.attribute){case"fill":jvm.isImageUrl(i[t].value)?a.css("background","url("+i[t].value+")"):a.css("background",i[t].value);break;case"stroke":a.css("background",i[t].value);break;case"image":a.css("background","url("+i[t].value+") no-repeat center center");break;case"r":jvm.$("<div/>").css({"border-radius":i[t].value,border:this.map.params.markerStyle.initial["stroke-width"]+"px "+this.map.params.markerStyle.initial.stroke+" solid",width:2*i[t].value+"px",height:2*i[t].value+"px",background:this.map.params.markerStyle.initial.fill}).appendTo(a)}e.append(a),s=i[t].label,this.params.labelRender&&(s=this.params.labelRender(s)),e.append(jvm.$("<div>"+s+" </div>").addClass("jvectormap-legend-tick-text")),n.append(e)}n.append(jvm.$("<div/>").css("clear","both"))},jvm.DataSeries=function(t,e,a){var s;t=t||{},t.attribute=t.attribute||"fill",this.elements=e,this.params=t,this.map=a,t.attributes&&this.setAttributes(t.attributes),jvm.$.isArray(t.scale)?(s="fill"===t.attribute||"stroke"===t.attribute?jvm.ColorScale:jvm.NumericScale,this.scale=new s(t.scale,t.normalizeFunction,t.min,t.max)):t.scale?this.scale=new jvm.OrdinalScale(t.scale):this.scale=new jvm.SimpleScale(t.scale),this.values=t.values||{},this.setValues(this.values),this.params.legend&&(this.legend=new jvm.Legend($.extend({map:this.map,series:this},this.params.legend)))},jvm.DataSeries.prototype={setAttributes:function(t,e){var a,s=t;if("string"==typeof t)this.elements[t]&&this.elements[t].setStyle(this.params.attribute,e);else for(a in s)this.elements[a]&&this.elements[a].element.setStyle(this.params.attribute,s[a])},setValues:function(t){var e,a,s=-Number.MAX_VALUE,i=Number.MAX_VALUE,n={};if(this.scale instanceof jvm.OrdinalScale||this.scale instanceof jvm.SimpleScale)for(a in t)t[a]?n[a]=this.scale.getValue(t[a]):void 0!=this.elements[a]&&(n[a]=this.elements[a].element.style.initial[this.params.attribute]);else{if("undefined"==typeof this.params.min||"undefined"==typeof this.params.max)for(a in t)e=parseFloat(t[a]),e>s&&(s=e),i>e&&(i=e);"undefined"==typeof this.params.min?(this.scale.setMin(i),this.params.min=i):this.scale.setMin(this.params.min),"undefined"==typeof this.params.max?(this.scale.setMax(s),this.params.max=s):this.scale.setMax(this.params.max);for(a in t)"indexOf"!=a&&(e=parseFloat(t[a]),isNaN(e)?void 0!=this.elements[a]&&(n[a]=this.elements[a].element.style.initial[this.params.attribute]):n[a]=this.scale.getValue(e))}this.setAttributes(n),jvm.$.extend(this.values,t)},clear:function(){var t,e={};for(t in this.values)this.elements[t]&&(e[t]=this.elements[t].element.shape.style.initial[this.params.attribute]);this.setAttributes(e),this.values={}},setScale:function(t){this.scale.setScale(t),this.values&&this.setValues(this.values)},setNormalizeFunction:function(t){this.scale.setNormalizeFunction(t),this.values&&this.setValues(this.values)}},jvm.Proj={degRad:180/Math.PI,radDeg:Math.PI/180,radius:6381372,sgn:function(t){return t>0?1:0>t?-1:t},mill:function(t,e,a){return{x:this.radius*(e-a)*this.radDeg,y:-this.radius*Math.log(Math.tan((45+.4*t)*this.radDeg))/.8}},mill_inv:function(t,e,a){return{lat:(2.5*Math.atan(Math.exp(.8*e/this.radius))-5*Math.PI/8)*this.degRad,lng:(a*this.radDeg+t/this.radius)*this.degRad}},merc:function(t,e,a){return{x:this.radius*(e-a)*this.radDeg,y:-this.radius*Math.log(Math.tan(Math.PI/4+t*Math.PI/360))}},merc_inv:function(t,e,a){return{lat:(2*Math.atan(Math.exp(e/this.radius))-Math.PI/2)*this.degRad,lng:(a*this.radDeg+t/this.radius)*this.degRad}},aea:function(t,e,a){var s=0,i=a*this.radDeg,n=29.5*this.radDeg,r=45.5*this.radDeg,o=t*this.radDeg,h=e*this.radDeg,l=(Math.sin(n)+Math.sin(r))/2,m=Math.cos(n)*Math.cos(n)+2*l*Math.sin(n),c=l*(h-i),p=Math.sqrt(m-2*l*Math.sin(o))/l,d=Math.sqrt(m-2*l*Math.sin(s))/l;return{x:p*Math.sin(c)*this.radius,y:-(d-p*Math.cos(c))*this.radius}},aea_inv:function(t,e,a){var s=t/this.radius,i=e/this.radius,n=0,r=a*this.radDeg,o=29.5*this.radDeg,h=45.5*this.radDeg,l=(Math.sin(o)+Math.sin(h))/2,m=Math.cos(o)*Math.cos(o)+2*l*Math.sin(o),c=Math.sqrt(m-2*l*Math.sin(n))/l,p=Math.sqrt(s*s+(c-i)*(c-i)),d=Math.atan(s/(c-i));return{lat:Math.asin((m-p*p*l*l)/(2*l))*this.degRad,lng:(r+d/l)*this.degRad}},lcc:function(t,e,a){var s=0,i=a*this.radDeg,n=e*this.radDeg,r=33*this.radDeg,o=45*this.radDeg,h=t*this.radDeg,l=Math.log(Math.cos(r)*(1/Math.cos(o)))/Math.log(Math.tan(Math.PI/4+o/2)*(1/Math.tan(Math.PI/4+r/2))),m=Math.cos(r)*Math.pow(Math.tan(Math.PI/4+r/2),l)/l,c=m*Math.pow(1/Math.tan(Math.PI/4+h/2),l),p=m*Math.pow(1/Math.tan(Math.PI/4+s/2),l);return{x:c*Math.sin(l*(n-i))*this.radius,y:-(p-c*Math.cos(l*(n-i)))*this.radius}},lcc_inv:function(t,e,a){var s=t/this.radius,i=e/this.radius,n=0,r=a*this.radDeg,o=33*this.radDeg,h=45*this.radDeg,l=Math.log(Math.cos(o)*(1/Math.cos(h)))/Math.log(Math.tan(Math.PI/4+h/2)*(1/Math.tan(Math.PI/4+o/2))),m=Math.cos(o)*Math.pow(Math.tan(Math.PI/4+o/2),l)/l,c=m*Math.pow(1/Math.tan(Math.PI/4+n/2),l),p=this.sgn(l)*Math.sqrt(s*s+(c-i)*(c-i)),d=Math.atan(s/(c-i));return{lat:(2*Math.atan(Math.pow(m/p,1/l))-Math.PI/2)*this.degRad,lng:(r+d/l)*this.degRad}}},jvm.MapObject=function(t){},jvm.MapObject.prototype.getLabelText=function(t){var e;return e=this.config.label?"function"==typeof this.config.label.render?this.config.label.render(t):t:null},jvm.MapObject.prototype.getLabelOffsets=function(t){var e;return this.config.label&&("function"==typeof this.config.label.offsets?e=this.config.label.offsets(t):"object"==typeof this.config.label.offsets&&(e=this.config.label.offsets[t])),e||[0,0]},jvm.MapObject.prototype.setHovered=function(t){this.isHovered!==t&&(this.isHovered=t,this.shape.isHovered=t,this.shape.updateStyle(),this.label&&(this.label.isHovered=t,this.label.updateStyle()))},jvm.MapObject.prototype.setSelected=function(t){this.isSelected!==t&&(this.isSelected=t,this.shape.isSelected=t,this.shape.updateStyle(),this.label&&(this.label.isSelected=t,this.label.updateStyle()),jvm.$(this.shape).trigger("selected",[t]))},jvm.MapObject.prototype.setStyle=function(){this.shape.setStyle.apply(this.shape,arguments)},jvm.MapObject.prototype.remove=function(){this.shape.remove(),this.label&&this.label.remove()},jvm.Region=function(t){var e,a,s;this.config=t,this.map=this.config.map,this.shape=t.canvas.addPath({d:t.path,"data-code":t.code},t.style,t.canvas.rootElement),this.shape.addClass("jvectormap-region jvectormap-element"),e=this.shape.getBBox(),a=this.getLabelText(t.code),this.config.label&&a&&(s=this.getLabelOffsets(t.code),this.labelX=e.x+e.width/2+s[0],this.labelY=e.y+e.height/2+s[1],this.label=t.canvas.addText({text:a,"text-anchor":"middle","alignment-baseline":"central",x:this.labelX,y:this.labelY,"data-code":t.code},t.labelStyle,t.labelsGroup),this.label.addClass("jvectormap-region jvectormap-element"))},jvm.inherits(jvm.Region,jvm.MapObject),jvm.Region.prototype.updateLabelPosition=function(){this.label&&this.label.set({x:this.labelX*this.map.scale+this.map.transX*this.map.scale,y:this.labelY*this.map.scale+this.map.transY*this.map.scale})},jvm.Marker=function(t){var e;this.config=t,this.map=this.config.map,this.isImage=!!this.config.style.initial.image,this.createShape(),e=this.getLabelText(t.index),this.config.label&&e&&(this.offsets=this.getLabelOffsets(t.index),this.labelX=t.cx/this.map.scale-this.map.transX,this.labelY=t.cy/this.map.scale-this.map.transY,this.label=t.canvas.addText({text:e,"data-index":t.index,dy:"0.6ex",x:this.labelX,y:this.labelY},t.labelStyle,t.labelsGroup),this.label.addClass("jvectormap-marker jvectormap-element"))},jvm.inherits(jvm.Marker,jvm.MapObject),jvm.Marker.prototype.createShape=function(){var t=this;this.shape&&this.shape.remove(),this.shape=this.config.canvas[this.isImage?"addImage":"addCircle"]({"data-index":this.config.index,cx:this.config.cx,cy:this.config.cy},this.config.style,this.config.group),this.shape.addClass("jvectormap-marker jvectormap-element"),this.isImage&&jvm.$(this.shape.node).on("imageloaded",function(){t.updateLabelPosition()})},jvm.Marker.prototype.updateLabelPosition=function(){this.label&&this.label.set({x:this.labelX*this.map.scale+this.offsets[0]+this.map.transX*this.map.scale+5+(this.isImage?(this.shape.width||0)/2:this.shape.properties.r),y:this.labelY*this.map.scale+this.map.transY*this.map.scale+this.offsets[1]})},jvm.Marker.prototype.setStyle=function(t,e){var a;jvm.Marker.parentClass.prototype.setStyle.apply(this,arguments),"r"===t&&this.updateLabelPosition(),a=!!this.shape.get("image"),a!=this.isImage&&(this.isImage=a,this.config.style=jvm.$.extend(!0,{},this.shape.style),this.createShape())},jvm.Map=function(t){var e,a=this;if(this.params=jvm.$.extend(!0,{},jvm.Map.defaultParams,t),!jvm.Map.maps[this.params.map])throw new Error("Attempt to use map which was not loaded: "+this.params.map);this.mapData=jvm.Map.maps[this.params.map],this.markers={},this.regions={},this.regionsColors={},this.regionsData={},this.container=jvm.$("<div>").addClass("jvectormap-container"),this.params.container&&this.params.container.append(this.container),this.container.data("mapObject",this),this.defaultWidth=this.mapData.width,this.defaultHeight=this.mapData.height,this.setBackgroundColor(this.params.backgroundColor),this.onResize=function(){a.updateSize()},jvm.$(window).resize(this.onResize);for(e in jvm.Map.apiEvents)this.params[e]&&this.container.bind(jvm.Map.apiEvents[e]+".jvectormap",this.params[e]);this.canvas=new jvm.VectorCanvas(this.container[0],this.width,this.height),("ontouchstart"in window||window.DocumentTouch&&document instanceof DocumentTouch)&&this.params.bindTouchEvents&&this.bindContainerTouchEvents(),this.bindContainerEvents(),this.bindElementEvents(),this.createTip(),this.params.zoomButtons&&this.bindZoomButtons(),this.createRegions(),this.createMarkers(this.params.markers||{}),this.updateSize(),this.params.focusOn&&("string"==typeof this.params.focusOn?this.params.focusOn={region:this.params.focusOn}:jvm.$.isArray(this.params.focusOn)&&(this.params.focusOn={regions:this.params.focusOn}),this.setFocus(this.params.focusOn)),this.params.selectedRegions&&this.setSelectedRegions(this.params.selectedRegions),this.params.selectedMarkers&&this.setSelectedMarkers(this.params.selectedMarkers),this.legendCntHorizontal=jvm.$("<div/>").addClass("jvectormap-legend-cnt jvectormap-legend-cnt-h"),this.legendCntVertical=jvm.$("<div/>").addClass("jvectormap-legend-cnt jvectormap-legend-cnt-v"),this.container.append(this.legendCntHorizontal),this.container.append(this.legendCntVertical),this.params.series&&this.createSeries()},jvm.Map.prototype={transX:0,transY:0,scale:1,baseTransX:0,baseTransY:0,baseScale:1.2,width:0,height:0,setBackgroundColor:function(t){this.container.css("background-color",t)},resize:function(){var t=this.baseScale;this.width/this.height>this.defaultWidth/this.defaultHeight?(this.baseScale=this.height/this.defaultHeight,this.baseTransX=Math.abs(this.width-this.defaultWidth*this.baseScale)/(2*this.baseScale)):(this.baseScale=this.width/this.defaultWidth,this.baseTransY=Math.abs(this.height-this.defaultHeight*this.baseScale)/(2*this.baseScale)),this.scale*=this.baseScale/t,this.transX*=this.baseScale/t,this.transY*=this.baseScale/t},updateSize:function(){this.width=this.container.width(),this.height=this.container.height(),this.resize(),this.canvas.setSize(this.width,this.height),this.applyTransform()},
reset:function(){var t,e;for(t in this.series)for(e=0;e<this.series[t].length;e++)this.series[t][e].clear();this.scale=this.baseScale,this.transX=this.baseTransX,this.transY=this.baseTransY,this.applyTransform()},applyTransform:function(){var t,e,a,s;if(this.defaultWidth*this.scale<=this.width?(t=(this.width-this.defaultWidth*this.scale)/(2*this.scale),a=(this.width-this.defaultWidth*this.scale)/(2*this.scale)):(t=0,a=(this.width-this.defaultWidth*this.scale)/this.scale),this.defaultHeight*this.scale<=this.height?(e=(this.height-this.defaultHeight*this.scale)/(2*this.scale),s=(this.height-this.defaultHeight*this.scale)/(2*this.scale)):(e=0,s=(this.height-this.defaultHeight*this.scale)/this.scale),this.transY>e?this.transY=e:this.transY<s&&(this.transY=s),this.transX>t?this.transX=t:this.transX<a&&(this.transX=a),this.canvas.applyTransformParams(this.scale,this.transX,this.transY),this.markers){this.container.find("g:eq(2)").css("visibility","hidden");var i=this;waitForFinalEvent(function(){i.repositionMarkers(),i.container.find("g:eq(2)").css("visibility","visible")},80,"repositionMarkers")}this.repositionLabels(),this.container.trigger("viewportChange",[this.scale/this.baseScale,this.transX,this.transY])},bindContainerEvents:function(){var t,e,a=!1,s=this;this.params.panOnDrag&&(this.container.mousemove(function(i){return a&&(s.transX-=(t-i.pageX)/s.scale,s.transY-=(e-i.pageY)/s.scale,s.applyTransform(),t=i.pageX,e=i.pageY),!1}).mousedown(function(s){return a=!0,t=s.pageX,e=s.pageY,!1}),this.onContainerMouseUp=function(){a=!1},jvm.$("body").mouseup(this.onContainerMouseUp)),this.params.zoomOnScroll&&this.container.mousewheel(function(t,e,a,i){var n=jvm.$(s.container).offset(),r=t.pageX-n.left,o=t.pageY-n.top,h=Math.pow(1+s.params.zoomOnScrollSpeed/1e3,t.deltaFactor*t.deltaY);s.tip.hide(),s.setScale(s.scale*h,r,o),t.preventDefault()})},bindContainerTouchEvents:function(){var t,e,a,s,i,n,r,o=this,h=function(h){var l,m,c,p,d=h.originalEvent.touches;"touchstart"==h.type&&(r=0),1==d.length?(1==r&&(c=o.transX,p=o.transY,o.transX-=(a-d[0].pageX)/o.scale,o.transY-=(s-d[0].pageY)/o.scale,o.applyTransform(),o.tip.hide(),(c!=o.transX||p!=o.transY)&&h.preventDefault()),a=d[0].pageX,s=d[0].pageY):2==d.length&&(2==r?(m=Math.sqrt(Math.pow(d[0].pageX-d[1].pageX,2)+Math.pow(d[0].pageY-d[1].pageY,2))/e,o.setScale(t*m,i,n),o.tip.hide(),h.preventDefault()):(l=jvm.$(o.container).offset(),i=d[0].pageX>d[1].pageX?d[1].pageX+(d[0].pageX-d[1].pageX)/2:d[0].pageX+(d[1].pageX-d[0].pageX)/2,n=d[0].pageY>d[1].pageY?d[1].pageY+(d[0].pageY-d[1].pageY)/2:d[0].pageY+(d[1].pageY-d[0].pageY)/2,i-=l.left,n-=l.top,t=o.scale,e=Math.sqrt(Math.pow(d[0].pageX-d[1].pageX,2)+Math.pow(d[0].pageY-d[1].pageY,2)))),r=d.length};jvm.$(this.container).bind("touchstart",h),jvm.$(this.container).bind("touchmove",h)},bindElementEvents:function(){var t,e=this;this.container.mousemove(function(){t=!0}),this.container.delegate("[class~='jvectormap-element']","mouseover mouseout",function(t){var a=jvm.$(this).attr("class").baseVal||jvm.$(this).attr("class"),s=-1===a.indexOf("jvectormap-region")?"marker":"region",i=jvm.$(this).attr("region"==s?"data-code":"data-index"),n="region"==s?e.regions[i].element:e.markers[i].element,r="region"==s?e.mapData.paths[i].name:e.markers[i].config.name||"",o=jvm.$.Event(s+"TipShow.jvectormap"),h=jvm.$.Event(s+"Over.jvectormap");"mouseover"==t.type?(e.container.trigger(h,[i]),h.isDefaultPrevented()||n.setHovered(!0),e.tip.text(r),e.container.trigger(o,[e.tip,i]),o.isDefaultPrevented()||(e.tip.show(),e.tipWidth=e.tip.width(),e.tipHeight=e.tip.height())):(n.setHovered(!1),e.tip.hide(),e.container.trigger(s+"Out.jvectormap",[i]))}),this.container.delegate("[class~='jvectormap-element']","mousedown",function(){t=!1}),this.container.delegate("[class~='jvectormap-element']","mouseup",function(){var a=jvm.$(this).attr("class").baseVal?jvm.$(this).attr("class").baseVal:jvm.$(this).attr("class"),s=-1===a.indexOf("jvectormap-region")?"marker":"region",i=jvm.$(this).attr("region"==s?"data-code":"data-index"),n=jvm.$.Event(s+"Click.jvectormap"),r="region"==s?e.regions[i].element:e.markers[i].element;t||(e.container.trigger(n,[i]),("region"===s&&e.params.regionsSelectable||"marker"===s&&e.params.markersSelectable)&&(n.isDefaultPrevented()||(e.params[s+"sSelectableOne"]&&e.clearSelected(s+"s"),r.setSelected(!r.isSelected))))})},bindZoomButtons:function(){var t=this;jvm.$("<div/>").addClass("jvectormap-zoomin").text("+").appendTo(this.container),jvm.$("<div/>").addClass("jvectormap-zoomout").html("&#x2212;").appendTo(this.container),this.container.find(".jvectormap-zoomin").click(function(){t.setScale(t.scale*t.params.zoomStep,t.width/2,t.height/2,!1,t.params.zoomAnimate)}),this.container.find(".jvectormap-zoomout").click(function(){t.setScale(t.scale/t.params.zoomStep,t.width/2,t.height/2,!1,t.params.zoomAnimate)}),this.container.find("svg").dblclick(function(e){var a=jvm.$(t.container).offset(),s=e.pageX-a.left,i=e.pageY-a.top;t.setScale(t.scale*t.params.zoomStep,s,i,!1,t.params.zoomAnimate)})},createTip:function(){var t=this;this.tip=jvm.$("<div/>").addClass("jvectormap-tip").appendTo(jvm.$("body")),this.container.mousemove(function(e){var a=e.pageX-15-t.tipWidth,s=e.pageY-15-t.tipHeight;5>a&&(a=e.pageX+15),5>s&&(s=e.pageY+15),t.tip.css({left:a,top:s})})},setScale:function(t,e,a,s,i){var n,r,o,h,l,m,c,p,d,u,v=jvm.$.Event("zoom.jvectormap"),g=this,f=0,j=Math.abs(Math.round(60*(t-this.scale)/Math.max(t,this.scale))),y=new jvm.$.Deferred;return t>this.params.zoomMax*this.baseScale?t=this.params.zoomMax*this.baseScale:t<this.params.zoomMin*this.baseScale&&(t=this.params.zoomMin*this.baseScale),"undefined"!=typeof e&&"undefined"!=typeof a&&(u=t/this.scale,s?(p=e+this.defaultWidth*(this.width/(this.defaultWidth*t))/2,d=a+this.defaultHeight*(this.height/(this.defaultHeight*t))/2):(p=this.transX-(u-1)/t*e,d=this.transY-(u-1)/t*a)),i&&j>0?(r=this.scale,o=(t-r)/j,h=this.transX*this.scale,m=this.transY*this.scale,l=(p*t-h)/j,c=(d*t-m)/j,n=setInterval(function(){f+=1,g.scale=r+o*f,g.transX=(h+l*f)/g.scale,g.transY=(m+c*f)/g.scale,g.applyTransform(),f==j&&(clearInterval(n),g.container.trigger(v,[t/g.baseScale]),y.resolve())},10)):(this.transX=p,this.transY=d,this.scale=t,this.applyTransform(),this.container.trigger(v,[t/this.baseScale]),y.resolve()),y},setFocus:function(t){var e,a,s,i,n,r;if(t=t||{},t.region?i=[t.region]:t.regions&&(i=t.regions),i){for(n=0;n<i.length;n++)this.regions[i[n]]&&(a=this.regions[i[n]].element.shape.getBBox(),a&&("undefined"==typeof e?e=a:(s={x:Math.min(e.x,a.x),y:Math.min(e.y,a.y),width:Math.max(e.x+e.width,a.x+a.width)-Math.min(e.x,a.x),height:Math.max(e.y+e.height,a.y+a.height)-Math.min(e.y,a.y)},e=s)));return this.setScale(Math.min(this.width/e.width,this.height/e.height),-(e.x+e.width/2),-(e.y+e.height/2),!0,t.animate)}return t.lat&&t.lng?(r=this.latLngToPoint(t.lat,t.lng),t.x=this.transX-r.x/this.scale,t.y=this.transY-r.y/this.scale):t.x&&t.y&&(t.x*=-this.defaultWidth,t.y*=-this.defaultHeight),this.setScale(t.scale*this.baseScale,t.x,t.y,!0,t.animate)},getSelected:function(t){var e,a=[];for(e in this[t])this[t][e].element.isSelected&&a.push(e);return a},getSelectedRegions:function(){return this.getSelected("regions")},getSelectedMarkers:function(){return this.getSelected("markers")},setSelected:function(t,e){var a;if("object"!=typeof e&&(e=[e]),jvm.$.isArray(e))for(a=0;a<e.length;a++)this[t][e[a]].element.setSelected(!0);else for(a in e)this[t][a].element.setSelected(!!e[a])},setSelectedRegions:function(t){this.setSelected("regions",t)},setSelectedMarkers:function(t){this.setSelected("markers",t)},clearSelected:function(t){var e,a={},s=this.getSelected(t);for(e=0;e<s.length;e++)a[s[e]]=!1;this.setSelected(t,a)},clearSelectedRegions:function(){this.clearSelected("regions")},clearSelectedMarkers:function(){this.clearSelected("markers")},getMapObject:function(){return this},getRegionName:function(t){return this.mapData.paths[t].name},createRegions:function(){var t,e,a=this;this.regionLabelsGroup=this.regionLabelsGroup||this.canvas.addGroup();for(t in this.mapData.paths)e=new jvm.Region({map:this,path:this.mapData.paths[t].path,code:t,style:jvm.$.extend(!0,{},this.params.regionStyle),labelStyle:jvm.$.extend(!0,{},this.params.regionLabelStyle),canvas:this.canvas,labelsGroup:this.regionLabelsGroup,label:"vml"!=this.canvas.mode?this.params.labels&&this.params.labels.regions:null}),jvm.$(e.shape).bind("selected",function(t,e){a.container.trigger("regionSelected.jvectormap",[jvm.$(this.node).attr("data-code"),e,a.getSelectedRegions()])}),this.regions[t]={element:e,config:this.mapData.paths[t]}},createMarkers:function(t){var e,a,s,i,n,r=this;if(this.markersGroup=this.markersGroup||this.canvas.addGroup(),this.markerLabelsGroup=this.markerLabelsGroup||this.canvas.addGroup(),jvm.$.isArray(t))for(n=t.slice(),t={},e=0;e<n.length;e++)t[e]=n[e];for(e in t)i=t[e]instanceof Array?{latLng:t[e]}:t[e],s=this.getMarkerPosition(i),s!==!1&&(a=new jvm.Marker({map:this,style:jvm.$.extend(!0,{},this.params.markerStyle,{initial:i.style||{}}),labelStyle:jvm.$.extend(!0,{},this.params.markerLabelStyle),index:e,cx:s.x,cy:s.y,group:this.markersGroup,canvas:this.canvas,labelsGroup:this.markerLabelsGroup,label:"vml"!=this.canvas.mode?this.params.labels&&this.params.labels.markers:null}),jvm.$(a.shape).bind("selected",function(t,e){r.container.trigger("markerSelected.jvectormap",[jvm.$(this.node).attr("data-index"),e,r.getSelectedMarkers()])}),this.markers[e]&&this.removeMarkers([e]),this.markers[e]={element:a,config:i})},repositionMarkers:function(){var t,e;for(t in this.markers)e=this.getMarkerPosition(this.markers[t].config),e!==!1&&this.markers[t].element.setStyle({cx:e.x,cy:e.y})},repositionLabels:function(){var t;for(t in this.regions)this.regions[t].element.updateLabelPosition();for(t in this.markers)this.markers[t].element.updateLabelPosition()},getMarkerPosition:function(t){return jvm.Map.maps[this.params.map].projection?this.latLngToPoint.apply(this,t.latLng||[0,0]):{x:t.coords[0]*this.scale+this.transX*this.scale,y:t.coords[1]*this.scale+this.transY*this.scale}},addMarker:function(t,e,a){var s,i,n={},r=[],a=a||[];for(n[t]=e,i=0;i<a.length;i++)s={},"undefined"!=typeof a[i]&&(s[t]=a[i]),r.push(s);this.addMarkers(n,r)},addMarkers:function(t,e){var a;for(e=e||[],this.createMarkers(t),a=0;a<e.length;a++)this.series.markers[a].setValues(e[a]||{})},removeMarkers:function(t){var e;for(e=0;e<t.length;e++)this.markers[t[e]].element.remove(),delete this.markers[t[e]]},removeAllMarkers:function(){var t,e=[];for(t in this.markers)e.push(t);this.removeMarkers(e)},latLngToPoint:function(t,e){var a,s,i,n=jvm.Map.maps[this.params.map].projection,r=n.centralMeridian;return-180+r>e&&(e+=360),a=jvm.Proj[n.type](t,e,r),s=this.getInsetForPoint(a.x,a.y),s?(i=s.bbox,a.x=(a.x-i[0].x)/(i[1].x-i[0].x)*s.width*this.scale,a.y=(a.y-i[0].y)/(i[1].y-i[0].y)*s.height*this.scale,{x:a.x+this.transX*this.scale+s.left*this.scale,y:a.y+this.transY*this.scale+s.top*this.scale}):!1},pointToLatLng:function(t,e){var a,s,i,n,r,o=jvm.Map.maps[this.params.map].projection,h=o.centralMeridian,l=jvm.Map.maps[this.params.map].insets;for(a=0;a<l.length;a++)if(s=l[a],i=s.bbox,n=t-(this.transX*this.scale+s.left*this.scale),r=e-(this.transY*this.scale+s.top*this.scale),n=n/(s.width*this.scale)*(i[1].x-i[0].x)+i[0].x,r=r/(s.height*this.scale)*(i[1].y-i[0].y)+i[0].y,n>i[0].x&&n<i[1].x&&r>i[0].y&&r<i[1].y)return jvm.Proj[o.type+"_inv"](n,-r,h);return!1},getInsetForPoint:function(t,e){var a,s,i=jvm.Map.maps[this.params.map].insets;for(a=0;a<i.length;a++)if(s=i[a].bbox,t>s[0].x&&t<s[1].x&&e>s[0].y&&e<s[1].y)return i[a]},createSeries:function(){var t,e;this.series={markers:[],regions:[]};for(e in this.params.series)for(t=0;t<this.params.series[e].length;t++)this.series[e][t]=new jvm.DataSeries(this.params.series[e][t],this[e],this)},remove:function(){this.tip.remove(),this.container.remove(),jvm.$(window).unbind("resize",this.onResize),jvm.$("body").unbind("mouseup",this.onContainerMouseUp)}},jvm.Map.maps={},jvm.Map.defaultParams={map:"world_mill_en",backgroundColor:"#505050",zoomButtons:!0,zoomOnScroll:!0,zoomOnScrollSpeed:3,panOnDrag:!0,zoomMax:8,zoomMin:1,zoomStep:1.6,zoomAnimate:!0,regionsSelectable:!1,markersSelectable:!1,bindTouchEvents:!0,regionStyle:{initial:{fill:"white","fill-opacity":1,stroke:"none","stroke-width":0,"stroke-opacity":1},hover:{"fill-opacity":.8,cursor:"pointer"},selected:{fill:"yellow"},selectedHover:{}},regionLabelStyle:{initial:{"font-family":"Verdana","font-size":"12","font-weight":"bold",cursor:"default",fill:"black"},hover:{cursor:"pointer"}},markerStyle:{initial:{fill:"grey",stroke:"#505050","fill-opacity":1,"stroke-width":1,"stroke-opacity":1,r:5},hover:{stroke:"black","stroke-width":2,cursor:"pointer"},selected:{fill:"blue"},selectedHover:{}},markerLabelStyle:{initial:{"font-family":"Verdana","font-size":"12","font-weight":"bold",cursor:"default",fill:"black"},hover:{cursor:"pointer"}}},jvm.Map.apiEvents={onRegionTipShow:"regionTipShow",onRegionOver:"regionOver",onRegionOut:"regionOut",onRegionClick:"regionClick",onRegionSelected:"regionSelected",onMarkerTipShow:"markerTipShow",onMarkerOver:"markerOver",onMarkerOut:"markerOut",onMarkerClick:"markerClick",onMarkerSelected:"markerSelected",onViewportChange:"viewportChange"},jvm.MultiMap=function(t){var e=this;this.maps={},this.params=jvm.$.extend(!0,{},jvm.MultiMap.defaultParams,t),this.params.maxLevel=this.params.maxLevel||Number.MAX_VALUE,this.params.main=this.params.main||{},this.params.main.multiMapLevel=0,this.history=[this.addMap(this.params.main.map,this.params.main)],this.defaultProjection=this.history[0].mapData.projection.type,this.mapsLoaded={},this.params.container.css({position:"relative"}),this.backButton=jvm.$("<div/>").addClass("jvectormap-goback").text("Back").appendTo(this.params.container),this.backButton.hide(),this.backButton.click(function(){e.goBack()}),this.spinner=jvm.$("<div/>").addClass("jvectormap-spinner").appendTo(this.params.container),this.spinner.hide()},jvm.MultiMap.prototype={addMap:function(t,e){var a=jvm.$("<div/>").css({width:"100%",height:"100%"});return this.params.container.append(a),this.maps[t]=new jvm.Map(jvm.$.extend(e,{container:a})),this.params.maxLevel>e.multiMapLevel&&this.maps[t].container.on("regionClick.jvectormap",{scope:this},function(t,e){var a=t.data.scope,s=a.params.mapNameByCode(e,a);a.drillDownPromise&&"pending"===a.drillDownPromise.state()||a.drillDown(s,e)}),this.maps[t]},downloadMap:function(t){var e=this,a=jvm.$.Deferred();return this.mapsLoaded[t]?a.resolve():jvm.$.get(this.params.mapUrlByCode(t,this)).then(function(){e.mapsLoaded[t]=!0,a.resolve()},function(){a.reject()}),a},drillDown:function(t,e){var a=this.history[this.history.length-1],s=this,i=a.setFocus({region:e,animate:!0}),n=this.downloadMap(e);i.then(function(){"pending"===n.state()&&s.spinner.show()}),n.always(function(){s.spinner.hide()}),this.drillDownPromise=jvm.$.when(n,i),this.drillDownPromise.then(function(){a.params.container.hide(),s.maps[t]?s.maps[t].params.container.show():s.addMap(t,{map:t,multiMapLevel:a.params.multiMapLevel+1}),s.history.push(s.maps[t]),s.backButton.show()})},goBack:function(){var t=this.history.pop(),e=this.history[this.history.length-1],a=this;t.setFocus({scale:1,x:.5,y:.5,animate:!0}).then(function(){t.params.container.hide(),e.params.container.show(),e.updateSize(),1===a.history.length&&a.backButton.hide(),e.setFocus({scale:1,x:.5,y:.5,animate:!0})})}},jvm.MultiMap.defaultParams={mapNameByCode:function(t,e){return t.toLowerCase()+"_"+e.defaultProjection+"_en"},mapUrlByCode:function(t,e){return"jquery-jvectormap-data-"+t.toLowerCase()+"-"+e.defaultProjection+"-en.js"}};                                                jQuery.fn.vectorMap('addMap', 'world_mill_en',{"insets": [{"width": 900, "top": 0, "height": 440.70631074413296, "bbox": [{"y": -12671671.123330014, "x": -20004297.151525836}, {"y": 6930392.02513512, "x": 20026572.39474939}], "left": 0}], "paths": {}, "height": 440.70631074413296, "projection": {"type": "mill", "centralMeridian": 11.5}, "width": 900.0});                                                /**
* author Christopher Blum
* - based on the idea of Remy Sharp, http://remysharp.com/2009/01/26/element-in-view-event-plugin/
* - forked from http://github.com/zuk/jquery.inview/
*/
(function ($) {
  var inviewObjects = {}, viewportSize, viewportOffset,
      d = document, w = window, documentElement = d.documentElement, expando = $.expando, timer;

  $.event.special.inview = {
    add: function(data) {
      inviewObjects[data.guid + "-" + this[expando]] = { data: data, $element: $(this) };

      // Use setInterval in order to also make sure this captures elements within
      // "overflow:scroll" elements or elements that appeared in the dom tree due to
      // dom manipulation and reflow
      // old: $(window).scroll(checkInView);
      //
      // By the way, iOS (iPad, iPhone, ...) seems to not execute, or at least delays
      // intervals while the user scrolls. Therefore the inview event might fire a bit late there
      //
      // Don't waste cycles with an interval until we get at least one element that
      // has bound to the inview event.
      if (!timer && !$.isEmptyObject(inviewObjects)) {
         timer = setInterval(checkInView, 250);
      }
    },

    remove: function(data) {
      try { delete inviewObjects[data.guid + "-" + this[expando]]; } catch(e) {}

      // Clear interval when we no longer have any elements listening
      if ($.isEmptyObject(inviewObjects)) {
         clearInterval(timer);
         timer = null;
      }
    }
  };

  function getViewportSize() {
    var mode, domObject, size = { height: w.innerHeight, width: w.innerWidth };

    // if this is correct then return it. iPad has compat Mode, so will
    // go into check clientHeight/clientWidth (which has the wrong value).
    if (!size.height) {
      mode = d.compatMode;
      if (mode || !$.support.boxModel) { // IE, Gecko
        domObject = mode === 'CSS1Compat' ?
          documentElement : // Standards
          d.body; // Quirks
        size = {
          height: domObject.clientHeight,
          width: domObject.clientWidth
        };
      }
    }

    return size;
  }

  function getViewportOffset() {
    return {
      top: w.pageYOffset || documentElement.scrollTop || d.body.scrollTop,
      left: w.pageXOffset || documentElement.scrollLeft || d.body.scrollLeft
    };
  }

  function checkInView() {
    var $elements = $(), elementsLength, i = 0;

    $.each(inviewObjects, function(i, inviewObject) {
      var selector = inviewObject.data.selector,
          $element = inviewObject.$element;
      $elements = $elements.add(selector ? $element.find(selector) : $element);
    });

    elementsLength = $elements.length;
    if (elementsLength) {
      viewportSize = viewportSize || getViewportSize();
      viewportOffset = viewportOffset || getViewportOffset();

      for (; i<elementsLength; i++) {
        // Ignore elements that are not in the DOM tree
        if (!$.contains(documentElement, $elements[i])) {
          continue;
        }

        var $element = $($elements[i]),
            elementSize = { height: $element.height(), width: $element.width() },
            elementOffset = $element.offset(),
            inView = $element.data('inview'),
            visiblePartX,
            visiblePartY,
            visiblePartsMerged;
        
        // Don't ask me why because I haven't figured out yet:
        // viewportOffset and viewportSize are sometimes suddenly null in Firefox 5.
        // Even though it sounds weird:
        // It seems that the execution of this function is interferred by the onresize/onscroll event
        // where viewportOffset and viewportSize are unset
        if (!viewportOffset || !viewportSize) {
          return;
        }
        
        if (elementOffset.top + elementSize.height > viewportOffset.top &&
            elementOffset.top < viewportOffset.top + viewportSize.height &&
            elementOffset.left + elementSize.width > viewportOffset.left &&
            elementOffset.left < viewportOffset.left + viewportSize.width) {
          visiblePartX = (viewportOffset.left > elementOffset.left ?
            'right' : (viewportOffset.left + viewportSize.width) < (elementOffset.left + elementSize.width) ?
            'left' : 'both');
          visiblePartY = (viewportOffset.top > elementOffset.top ?
            'bottom' : (viewportOffset.top + viewportSize.height) < (elementOffset.top + elementSize.height) ?
            'top' : 'both');
          visiblePartsMerged = visiblePartX + "-" + visiblePartY;
          if (!inView || inView !== visiblePartsMerged) {
            $element.data('inview', visiblePartsMerged).trigger('inview', [true, visiblePartX, visiblePartY]);
          }
        } else if (inView) {
          $element.data('inview', false).trigger('inview', [false]);
        }
      }
    }
  }

  $(w).bind("scroll resize", function() {
    viewportSize = viewportOffset = null;
  });
  
  // IE < 9 scrolls to focused elements without firing the "scroll" event
  if (!documentElement.addEventListener && documentElement.attachEvent) {
    documentElement.attachEvent("onfocusin", function() {
      viewportOffset = null;
    });
  }
})(jQuery);
}

/* Load jQuery */
/* "https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js" */
if ( 'clustrm_jq' in window ) {
    $ = jQuery = window.clustrm_jq;
    loadLibs();
    main();

} else {
    loadScript("https://code.jquery.com/jquery-1.12.4.min.js", function() {
        /* Restore $ and window.jQuery to their previous values and store the
          new jQuery in our local jQuery variables. */
        $ = jQuery = window.clustrm_jq = window.jQuery.noConflict(true);
        loadLibs();


        main();
    });
}

}(window, document)); /* end IIFE */

                            