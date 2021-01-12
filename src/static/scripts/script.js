'use strict';

function check_item(action){
    $.getJSON('/take_screenshot').done(function(data) {
        // Log returned data      
        let img_name = data.result;     
        $.post('/make_prediction', {
            img_name: img_name
        }).done(function(data) {
            let item = data.result;            

            if (action=='add') {
                // Add to db
                let cfm_window = confirm('Please confirm addtion of detected item: ${item}');
                if (cfm_window){
                    var num_items = prompt('Enter number of items to add: ', '1');
                    $.post('/add_to_db', {
                        item:item,
                        number:num_items
                    }).done(function(data) {
                        $.post('/delete_file', {
                            img_name:img_name
                        }).done(function(data) {
                            console.log(data);
                        })
                    })
                }
                else {
                    // Save to wrong predictions
                    $.post('/wrong_predictions', {
                        img_name:img_name
                    }).done(function(data){
                        console.log(data);
                    })
                }
            }
            else if (action=='remove') {
                let cfm_window = confirm('Please confirm removal of detected item: ${item}');
                if (cfm_window) {
                    $.post('/remove_from_db', {
                        item:item
                    }).done(function(data) {
                        $.post('/delete_file', {
                            img_name:img_name
                        }).done(function(data) {
                            console.log(data)
                        })
                    })
                }
                else {
                    // Save to wrong predictions
                    $.post('/wrong_predictions', {
                        img_name:img_name
                    }).done(function(data) {
                        console.log(data);
                    })
                }
            }
        }); 
    });
}

function check_stock() {
    $.getJSON('/check_stock', {
    }).done(function(data) {
        $.each(data.result, function(i,f) {
            let table_data = '';
            table_data = '<tr>' + '<td>' + f.item_type + '</td>' + 
                        '<td>' + f.number + '</td>' + '</tr>'
            $(table_data).appendTo('#stock_table tbody');
        })
        document.getElementById('table_div').style.display = 'block';
    })
}

// Run after webpage has loaded
$(document).ready(function() {
    $('#add').click(function() {
        check_item('add');
    });    
    $('#remove').click(function() {
        check_item('remove');
    });      
    $('#stock').click(function() {
        $('#table_body').empty();
        document.getElementById('table_div').style.display = 'none';
        check_stock();
    });
    $('#screenshot').click(function() {
        var number = prompt('Number of screenshots to take: ', '50');
        console.log(number);
        if (number==null){
            return;
        }
        else if (!parseInt(number) || parseInt(number)==0) {
            number = 50;
        }
        else {
            number = parseInt(number);
        }
        // $.get() is also possible, functions the same and allows other data types
        $.post('/bulk_screenshots', {
            number:number
        }).done(function(data) {
            alert('Screenshot completed')
            console.log(data);
        })
    });
});