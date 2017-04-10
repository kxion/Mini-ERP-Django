function myfunction(id, photo) {
	// console.log(id);
	console.log(photo);
	photo_path = "/media/" + photo;
	console.log(photo_path);
	
	// console.log(photo);
	// var productID = $("<div/>",{"text":id});
	var productIMG = $("<img/>",{"src":photo_path, style:"height:220px; float:left;"});
	$('#myhide').empty();
	$('#myhide').append(productIMG);
	$('#myhide').show();

}

$( document ).ready(function() {
    console.log( "create_purchase.js ready!!!!" );
    v1 = document.getElementById("test");
    $('#myhide').hide();
});
