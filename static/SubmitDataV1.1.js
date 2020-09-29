function submit_data(_submit_link) {
    var t = new Date().getHours()
    var entry_type = document.getElementById('entry_type').innerText
    if ((t > 10 && t < 18) && entry_type == "Manual") {
        alert('Data collection must be within 5 hrs of midnight.')
    } else {
        var all = document.getElementsByClassName('sub_item')
        for (var i = 0; i < all.length; i++) {
            elm = all[i]
            if (elm.value != "") {
                var data = Object.assign({}, elm.dataset)
                data['value'] = elm.value

                fetch(_submit_link, {
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    method: 'POST',
                    body: JSON.stringify(data)
                }).then(function (response) {
                    return response.text();
                }).then(function (text) {
                    console.log('POST response: ');
                    console.log(text);
                    //alert(text);
                })
            }
        }
    }

}