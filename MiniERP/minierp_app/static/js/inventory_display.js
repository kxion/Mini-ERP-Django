function show_product(name, photo, supplier, model, price, stock, dimension, weight, note) {
	// console.log(id);
	photo_path = "/media/" + photo;
	console.log(photo_path);
	console.log(name);
	console.log(supplier);
	if(model == '') model = 'None';
	console.log(model);
	console.log(price);
	console.log(stock);
	if(dimension == '') dimension = 'None';
	console.log(dimension);
	if(weight == '') weight = 'None';
	console.log(weight);
	if(note == '') note = 'None';
	console.log(note);
	var productIMG = $("<img/>",{"src":photo_path, style:"height:220px; float:left;"});
	var textBox1 = $("<div/>", {"class": "text-box"});
	var ul1 = $("<ul/>");
	var list = $("<li/>", {"text": "Product Name:"});
	var p = $("<p/>", {"text": name});
	ul1.append(list);
	ul1.append(p);
	list = $("<li/>", {"text": "Product Model:"});
	p = $("<p/>", {"text": model});
	ul1.append(list);
	ul1.append(p);
	list = $("<li/>", {"text": "Product Dimention:"});
	p = $("<p/>", {"text": dimension});
	ul1.append(list);
	ul1.append(p);
	list = $("<li/>", {"text": "Product Weight:"});
	p = $("<p/>", {"text": weight});
	ul1.append(list);
	ul1.append(p);
	textBox1.append(ul1);

	var textBox2 = $("<div/>", {"class": "text-box"});
	var ul1 = $("<ul/>");
	var list = $("<li/>", {"text": "Product Supplier:"});
	var p = $("<p/>", {"text": supplier});
	ul1.append(list);
	ul1.append(p);
	list = $("<li/>", {"text": "Product Price:"});
	p = $("<p/>", {"text": price});
	ul1.append(list);
	ul1.append(p);
	list = $("<li/>", {"text": "In Stock:"});
	p = $("<p/>", {"text": stock});
	ul1.append(list);
	ul1.append(p);
	list = $("<li/>", {"text": "Note:"});
	p = $("<p/>", {"text": note});
	ul1.append(list);
	ul1.append(p);
	textBox2.append(ul1);
	
	$('#product_detail').empty();
	$('#product_detail').append(productIMG);
	$('#product_detail').append(textBox1);
	$('#product_detail').append(textBox2);
	$('#product_detail').show();

}

$( document ).ready(function() {
    console.log( "inventory_display.js ready!!!!" );
    $('#product_detail').hide();
});
