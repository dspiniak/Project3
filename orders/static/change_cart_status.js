var csrftoken = getCookie('csrftoken');

$(document).on('change', 'select', function() {
    // get select value
    status_selected = this.value;
    cart_id = this.id;
    console.log("User changed select: Cart id "+cart_id+", to new status: "+status_selected+", sending change request to server");

    let cart_status_to_server = new FormData();
    cart_status_to_server.append('status_selected', status_selected);
    cart_status_to_server.append('cart_id', cart_id);

    // request options from server
    var request = new Request(
      '/change_cart_status',
      {headers: {'X-CSRFToken': csrftoken}}
    );

    fetch(request,
      {
        method: 'POST',
        body: cart_status_to_server,
        mode: 'same-origin'
      })
      .then(response => {
        console.log("GOT CART STATUS RESPONSE FROM SERVER");
        return response.json();
      })
      .then(data => {
        alert(data.message);
      })
      .catch((err) => {
          console.log("Something went wrong!", err);
    });

  return;
});


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
