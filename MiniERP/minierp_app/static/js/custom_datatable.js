$(document).ready(function() {
	console.log("custom_datatable is ready!");
    $('#example').DataTable( {
        "scrollY": 215,
        "scrollX": true,
        "scrollCollapse": true,
        "fixedColumns": {
            leftColumns: 1,
        },   
    });

    $('#example2').DataTable( {
        "scrollY": 150,
        "scrollX": true,
        "scrollCollapse": true,
        "fixedColumns": {
            leftColumns: 1,
        },   
    });

    $('#example3').DataTable( {
        "scrollY": 170,
        "scrollX": true,
        "scrollCollapse": true,
        "fixedColumns": {
            leftColumns: 1,
        },   
    });

    $('#example4').DataTable( {
        "scrollY": 310,
        "scrollX": true,
        "scrollCollapse": true,
    });
});

