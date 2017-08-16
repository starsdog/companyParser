
var graph_json={
	'download':function(){
		var source=$('#graph_source').val();
		var uuid=$('#uuid').val();
		console.log(uuid);
		req_ajax({
			url: web_url+"/graph/download",
			data: {
                "source": source,                
                "uuid": uuid,
                "toGraph": 0
            },
            success: function(data){
            	var jsonse = JSON.stringify(data);
            	var blob = new Blob([jsonse], {            		
                    type: 'application/json'
                }),
                link = $('<a></a>').attr({
                    'download': uuid+'.json',
                    'href': window.URL.createObjectURL(blob)
                }).appendTo('body');

                link.get(0).click();
                link.remove();
            },
            error: function (data) {
            }
		});	
	}

}

var graph_area={		
	'submit':function(){
		d3.select("svg").remove(); 
    	var source=$('#graph_source').val();    
    	var uuid=$('#uuid').val();
    	    	
		var width = screen.width;
		var height = screen.height;
		var img_w = 77;
		var img_h = 90;
		
		var svg = d3.select("#relation_show").append("svg")
								.attr("width",width)
								.attr("height",height);
		
		req_ajax({
			url: web_url+"/graph/download",
			data: {
                "source": source,                
                "uuid": uuid,
                "toGraph": 1
            },
            success: function(data){            		
				var force = d3.layout.force()
								.nodes(data['nodes'])
								.links(data['edges'])
								.size([width,height])
								.linkDistance(100)
								.charge(-1500)
								.start();
								
				var edges_line = svg.selectAll("line")
									.data(data['edges'])
									.enter()
									.append("line")
									.style("stroke","#ccc")
									.style("stroke-width",1);
									
				var edges_text = svg.selectAll(".linetext")
									.data(data['edges'])
									.enter()
									.append("text")
									.attr("class","linetext")
									.text(function(d){
										return d.relation;
									});
				
				var color = d3.scale.linear()
					                .domain([1,30])
					                .range(['#f00', '#00f']);
										
				var nodes_img = svg.selectAll("circle")
									.data(data['nodes'])
									.enter()
									.append("circle")
									.attr("r",20)
									.style("fill",function(d,i){
										return color(i);
									})
									.on("mouseover",function(d,i){
										edges_text.style("fill-opacity",function(edge){
											if( edge.source === d || edge.target === d ){
												return 1.0;
											}
										});
									})
									.on("mouseout",function(d,i){
										edges_text.style("fill-opacity",function(edge){
											if( edge.source === d || edge.target === d ){
												return 0.0;
											}
										});
									})
									.call(force.drag);
				
				var text_dx = -20;
				var text_dy = 20;
				
				var nodes_text = svg.selectAll(".nodetext")
									.data(data['nodes'])
									.enter()
									.append("text")
									.attr("class","nodetext")
									.attr("dx",text_dx)
									.attr("dy",text_dy)
									.text(function(d){
										return d.name;
									});
				
									
				force.on("tick", function(){							
					//限制结点的边界
					/*
					root.nodes.forEach(function(d,i){
						d.x = d.x - img_w/2 < 0     ? img_w/2 : d.x ;
						d.x = d.x + img_w/2 > width ? width - img_w/2 : d.x ;
						d.y = d.y - img_h/2 < 0      ? img_h/2 : d.y ;
						d.y = d.y + img_h/2 + text_dy > height ? height - img_h/2 - text_dy : d.y ;
					});
				    */
				
					 edges_line.attr("x1",function(d){ return d.source.x; });
					 edges_line.attr("y1",function(d){ return d.source.y; });
					 edges_line.attr("x2",function(d){ return d.target.x; });
					 edges_line.attr("y2",function(d){ return d.target.y; });
					 					
					 edges_text.attr("x",function(d){ return (d.source.x + d.target.x) / 2 ; });
					 edges_text.attr("y",function(d){ return (d.source.y + d.target.y) / 2 ; });
					 				 
					 //update nodes position and text
					 nodes_img.attr("cx",function(d){ return d.x; })
					 		.attr("cy",function(d){ return d.y; });
					
					 nodes_text.attr("x",function(d){ return d.x });
					 nodes_text.attr("y",function(d){ return d.y + img_w/2; });				
				});							
            },
            error: function (data) {
            }
		});			
		
	}
}