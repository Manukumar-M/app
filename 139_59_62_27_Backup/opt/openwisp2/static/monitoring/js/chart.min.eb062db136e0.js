'use strict';(function($){window.createChart=function(data,x,id,title,type){if(data===false){alert(gettext('error while receiving data from server'));return;}
if(!x){x=data.x;}
var xaxis=data.xaxis||{};var yaxis=data.yaxis||{};xaxis.visible=type!='histogram';var mode=x.length>30?'lines':'markers+lines',layout={showlegend:true,legend:{orientation:'h',xanchor:'center',yanchor:'top',y:-0.15,x:0.5,traceorder:'normal'},xaxis:xaxis,yaxis:yaxis,margin:{l:50,r:50,b:15,t:20,pad:4},height:350,hovermode:'x unified'},charts=[],container=$('#'+id),plotlyContainer=container.find('.js-plotly-plot').get(0),notApplicable=gettext('N/A'),unit=data.unit,summaryLabels=[],fixedY=false,fixedYMax=100,help,tooltip,heading;if(data.colors){layout.colorway=data.colors;}
if(data.colorscale&&typeof(data.colorscale.fixed_value)!==undefined){layout.yaxis={visible:false};}else if(unit==='%'){fixedY=true;}
if(type==='histogram'){layout.hovermode='closest';}
if(type==='stackedbar'){type='bar';layout.barmode='stack';}
var map,mapped,label,fixedValue,key;function findInColorMap(value){var desc,color,controlVal,n,map=data.colorscale.map;if(!map){return false;}
for(n in map){controlVal=map[n][0];if(controlVal===null||value>=controlVal){color=map[n][1];desc=map[n][2];break;}}
return{color:color,desc:desc};}
for(var i=0;i<data.traces.length;i++){key=data.traces[i][0];label=data.traces[i][0].replace(/_/g,' ');if(data.summary_labels){summaryLabels.push([key,data.summary_labels[i]]);}
var options={name:label,type:type,mode:mode,fill:data.fill||'tozeroy',hovertemplate:[],y:[]},yValuesRaw=data.traces[i][1];if(type!=='histogram'){options.x=x;options.hoverinfo='x+y';}
else{options.x=[''];options.histfunc='sum';}
if(data.colorscale){var config=data.colorscale;map=data.colorscale.map;fixedValue=data.colorscale.fixed_value;options.marker={cmax:config.max,cmin:config.min,colorbar:{title:config.label},colorscale:config.scale,color:[]};if(map){layout.showlegend=false;layout.margin.b=45;}}
for(var c=0;c<yValuesRaw.length;c++){var val=yValuesRaw[c],shownVal=val,desc=label,hovertemplate;if(data.colorscale&&map){mapped=findInColorMap(val);if(typeof(fixedValue)!==undefined&&val!==null){val=fixedValue;}
options.marker.color.push(mapped.color);desc=mapped.desc;}
if(val===null){if(layout.yaxis.zeroline!==false){val=0;}
hovertemplate=notApplicable+'<extra></extra>';}
else{hovertemplate=shownVal+unit+'<extra>'+desc+'</extra>';}
if(fixedY&&val>fixedYMax){fixedYMax=val;}
options.y.push(val);options.hovertemplate.push(hovertemplate);}
charts.push(options);}
if(fixedY){layout.yaxis={range:[0,fixedYMax]};}
Plotly.newPlot(plotlyContainer,charts,layout,{responsive:true});container.find('.custom-legend').remove();if(data.colorscale&&data.colorscale.map){container.append('<div class="custom-legend"></div>');map=data.colorscale.map;var customLegend=container.find('.custom-legend');for(i=map.length-1;i>=0;i--){var color=map[i][1];label=map[i][2];customLegend.append('<div class="legend"><span style="background:'+color+'"></span> '+label+'</div>');}}
container.find('.circle').remove();if(data.summary&&type!='histogram'){for(i=0;i<summaryLabels.length;i++){var el=summaryLabels[i],percircleOptions={progressBarColor:data.colors[i]};key=el[0];label=el[1];var value=data.summary[key];if(unit==='%'){percircleOptions.percent=value;if(value===0){percircleOptions.text='0%';percircleOptions.percent=1;}}
else{percircleOptions.text=value+data.unit;percircleOptions.percent=75;}
if(value===null){percircleOptions.text='N/A';percircleOptions.percent=1;}
if(data.colorscale&&data.colorscale.map){mapped=findInColorMap(value);percircleOptions.progressBarColor=mapped.color;label=label+': '+mapped.desc;}
container.append('<div class="small circle" title="'+label+'"></div>');container.find('.circle').eq(-1).percircle(percircleOptions);}}
if(container.find('h3.chart-heading').length||!data.title){return;}
container.prepend('<h3 class="chart-heading"></h3>');heading=container.find('.chart-heading');heading.text(title);heading.append('<a class="chart-help">?</a>');help=heading.find('a');help.attr('title',gettext('Click to show chart description'));container.find('.svg-container').append('<p class="tooltip"></p>');tooltip=container.find('p.tooltip');tooltip.text(data.description);help.on('click',function(){tooltip.toggle();});};}(django.jQuery));