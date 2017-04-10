$( document ).ready(function() {
    console.log( "stock_color.js ready!!!!" );
    // var selector = document.getElementById("message");
	
	if(document.getElementById("stock_number")){
		stock = document.getElementById("stock_number");
		if(stock.innerHTML == "0 in stock"){
			stock.innerHTML = "out of stock"
			stock.style.color = "red";
		}
		else{
			stock.style.color = "green";
		}
	}
    
    var c1 = document.getElementById("abc123");
    if(c1 != null){
    	for(i = 0; i < c1.options.length; i++) {
	    	val = c1.options[i].innerHTML;
	    	index = val.indexOf('(');
	    	if(index != -1){
	    		val = val.substring(0, index);
	    		c1.options[i].innerHTML = val;
	    	}
	    	// c1.style.color = 'red';
	    	// c1.options[i].innerHTML = 'okokokokok';
	    	// document.getElementById("abc123").style.color = 'red';
	    	// console.log(c1.options[i].style.color);
	    	if(val.includes("out")){
	    		console.log("out!!!");
	    		// document.getElementById("abc123").style.color = 'red';
	    		c1.options[i].id += "redtext" ;
	    	}
	    	console.log(c1.options[i])
	    }
    } 
    
	
});
