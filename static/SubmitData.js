function submit_data(_submit_link) {
    var t = new Date().getHours()
    if (t > 10 && t < 6) {
        alert('Enter data after 6pm.')
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