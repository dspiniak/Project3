var csrftoken = getCookie('csrftoken');
var food_choice;
var size_choice;
var sizes = [];
var size_prices = {};
var toppings_prices = {};
var base_price;
var toppings_price = 0;
var order_price;
var toppings_choices = [];
var topping_num = 0;
var toppings = [];

// display size option based on user input
$(document).on('change', '#food_type', function() {

  reset();

  // fetch new option only if Pizza, Subs, or Dinner Platters
  food_choice = $( "#food_type option:selected").text()
  console.log("USER SELECTED FOOD: "+food_choice);

  if (food_choice.includes("Pizza") || food_choice.includes("Sub") || food_choice.includes("Dinner Platter")){
    // fetch size prices
    display_sizes(food_choice);
  }

  console.log("EXITING FOOD SELECTION ROUTINE")

  return;
});

// fetch toppings if necessary
$(document).on('change', '#size', function() {

  reset_toppings();
  size_choice = $( "#size option:selected").text();
  console.log("USER SELECTED SIZE: "+size_choice);

  if (food_choice.includes("Pizza") || food_choice.includes("Sub")){
    // fetch size prices
    display_toppings(food_choice, size_choice);
  }

  console.log("EXITING SIZE SELECTION ROUTINE")

  return;
});

// calculate price
$(document).on('change', '#size, #toppings', function() {

  if (food_choice.includes("Pizza")){
    if (size_choice != null){

      // display price
      base_price = size_prices[size_choice];

      // store toppings choices and update toppings price
      if ($('#toppings').val() != null){
        toppings_choices = $('#toppings').val();
        console.log("toppings_choices: "+toppings_choices+"; toppings_choices length: "+toppings_choices.length );
        if (toppings_choices.length > 3 || food_choice.includes("Special")){
          toppings_price = 0;
        }
        else{
          toppings_price = toppings_prices[toppings_choices.length];
        }
      }
    }

  } else if (food_choice.includes("Sub")){
      if (size_choice != null){

        // display price
        base_price = size_prices[size_choice];

        // store toppings choices and update toppings price
        if ($('#toppings').val() != null){
          toppings_choices = $('#toppings').val();
          console.log("toppings_choices: "+toppings_choices+"; toppings_choices length: "+toppings_choices.length );
          toppings_price = toppings_prices[1]*toppings_choices.length;
          }
        }
  } else if (food_choice.includes("Dinner Platter")){
    // do nothing
  } else if (food_choice.includes("Pasta") || food_choice.contains("Dinner Platter")){
    // do nothing
  }

  console.log("toppings price is: "+toppings_price);
  order_price = parseFloat(base_price)+parseFloat(toppings_price);
  console.log("display price: "+order_price);
  $('#order_price').text(order_price);

  return;
});

// maximum topping selection
$(document).on('change','#toppings', function() {
    if (food_choice.includes("Pizza") && food_choice.includes("Cheese")){
      var last_valid_selection = null;
      if ($(this).val().length > 3) {
        $(this).val(last_valid_selection);
      } else {
        last_valid_selection = $(this).val();
      }
    }

    if (food_choice.includes("Sub")){
      var last_valid_selection = null;
      if ($(this).val().length > 3) {
        $(this).val(last_valid_selection);
      } else {
        last_valid_selection = $(this).val();
      }
    }

});

// display select with sizes according to the selected food
function display_sizes(food_choice){

  // transform user input into form data to send to server
  let food_selection_toserver = new FormData();
  food_selection_toserver.append('food_choice', food_choice);

  // request options from server
  var request = new Request(
    '/load_sizes',
    {headers: {'X-CSRFToken': csrftoken}}
  );

  fetch(request,
    {
      method: 'POST',
      body: food_selection_toserver,
      mode: 'same-origin'
    })
    .then(response => {
      console.log("got size and toppings from server");
      return response.json()
    })
    .then(data => {

      let sizes_json = JSON.parse(data.sizes);
      console.log("got sizes from server:"+JSON.stringify(sizes_json));

      // transform size_prices to dict object
      $.each(sizes_json, function(i){
        sizes.push(sizes_json[i].fields.size);
        size_prices[sizes_json[i].fields.size] = sizes_json[i].fields.price;
      });

      console.log("transformed sizes to dict: "+JSON.stringify(sizes));

      console.log("transformed size_prices to dict: "+JSON.stringify(size_prices));

      display_select("size", sizes, false);

    }
    )
    .catch((err) => {
        console.log("Something went wrong!", err);
  });

  console.log("exiting display_sizes routine")
  return;
  };

// display select with toppings according to the selected food and size
function display_toppings(food_choice, size_choice = ""){
  console.log("entered display toppings function with food_choice: "+food_choice+" and size_choice: "+size_choice);

  // transform user input into form data to send to server
  let size_selection_toserver = new FormData();
  size_selection_toserver.append('food_choice', food_choice);
  size_selection_toserver.append('size_choice', size_choice);

  // request options from server
  var request = new Request(
    '/load_toppings',
    {headers: {'X-CSRFToken': csrftoken}}
  );

  fetch(request,
    {
      method: 'POST',
      body: size_selection_toserver,
      mode: 'same-origin'
    })
    .then(response => {
      console.log("got toppings from server");
      return response.json()
    })
    .then(data => {

      // get toppings from server
      let toppings_json = JSON.parse(data.toppings);
      console.log("GOT TOPPINGS FROM SERVER: "+JSON.stringify(toppings_json));

      // toppings = toppings_json[0].fields.toppings
      $.each(toppings_json[0].fields.toppings, function(i){
        toppings.push(toppings_json[0].fields.toppings[i]);
      });
      console.log("extracted toppings: "+JSON.stringify(toppings));

      // get toppings_prices from server
      let toppings_prices_json = JSON.parse(data.toppings_prices);
      console.log("GOT TOPPING PRICES FROM SERVER: "+JSON.stringify(toppings_prices_json));

      // transform to dict
      $.each(toppings_prices_json, function(i){
        let num = toppings_prices_json[i].fields.topping_num;
        let top = toppings_prices_json[i].fields.price;
        console.log(num+", "+top);
        toppings_prices[num] = top;
      });

      console.log("transformed toppings_prices to dict: "+JSON.stringify(toppings_prices));

      display_select("toppings", toppings, true);

    }
    )
    .catch((err) => {
        console.log("Something went wrong!", err);
  });

  return;
};

// display a select object, function takes the id for the select and the options it should display
function display_select(select_name, select_options, multiple_select){

  // create div with toppings selects
  const div = document.createElement('div');
  div.id = select_name+'_div';

  // create multiple select object
  var select_object = document.createElement('select');
  select_object.multiple = multiple_select;
  select_object.id = select_name;
  select_object.name = select_name;
  select_object.className = 'form-control';

  // create text to display before select
  var select_text = document.createElement('span');
  select_text.innerHTML = 'Select your '+select_name;
  div.appendChild(select_text);
  div.appendChild(select_object);

  form_div.appendChild(div);

  // add empty option-- to select
  $('#'+select_name).append(new Option("-", "--"));
  // $('#'+select_name).options["-"].disabled = true;

  // iterate through options and add them to select
  console.log("will loop this:"+JSON.stringify(select_options));
  for (key in select_options) {
    $('#'+select_name).append(new Option(select_options[key], select_options[key]));
  }

  // when toppings clicked update toppings_price
  if (select_name == "size"){
    select_object.required = true;
  }

  console.log("exiting display select routine")
  return;
}

function reset(){
  // if sizes or toppings were selectd, delete them
  console.log("INTO RESETTING FIELDS");

  food_choice = "";
  base_price = 0;

  $("#size_div").remove();
  size_choice = "";
  size_prices = {};
  sizes = [];

  $("#toppings_div").remove();
  toppings = [];
  toppings_choices = [];
  topping_num = 0;
  toppings_prices = [];
  toppings_price = 0;

  order_price = 0;
}

function reset_toppings(){
  $("#toppings_div").remove();
  toppings_prices = [];
  toppings = [];
  toppings_choices = [];
  topping_num = 0;
}
// enable csrftoken via getcookie function
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
