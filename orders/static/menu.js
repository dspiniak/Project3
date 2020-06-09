document.addEventListener('DOMContentLoaded', () => {
  // 1) create first form element depending on food_type selection

      // when user selects food option selected by user and display next option based on logic using multiple if's

  // var food_type =
  $('#food_type').change(function() {
    console.log("hola");
    // send and retrieve options from server
    // var request_options = new XMLHttpRequest();
    // request_options.open('POST', '/load_options');

    const options_to_server = new FormData();
    options_to_server.append('csrfmiddlewaretoken', '{{ csrf_token }}');
    options_to_server.append('food_type', food_type);
    $.ajax({
        url: '/load_options',  //server script to process data
        type: 'POST',
        data: options_to_server,
        processData: false,
        contentType: false,
        success: function(response){
          const data = JSON.parse(response.responseText);
          console.log("hola");
          if (data.success) {

          const size_div = document.createElement('div');
          size_div.id = 'size';
          var size_select = document.createElement('SELECT');
          data.size_price.forEach(size_price =>{

            // CREATE SIZE OPTIONS
            var option = document.createElement('option');
            option.text = size_price;
            size_select.add(option);
            // display toppings

            });
          }
        }
    });
    // request_options.send(options_to_server);

    // When server responds



      // get options
      // add size options, via retrieving options from server and then adding them to the selec

  });



    // display total price according to selections




});
