function togglePopup(item_id) {
    document.getElementById("popup-1").classList.toggle("active");
    if (item_id != null) {
        var y = document.getElementById(item_id)
        var innerHTML = `<div style="text-align: left;">`
        var j = 0
        for (i in y.dataset) {
            if (!(i.includes('id'))) {
                j += 1
                innerHTML += `${i.charAt(0).toUpperCase() + i.slice(1)}: <b>${y.dataset[i]}</b>`
                if (j % 2 == 0) {
                    innerHTML += '<br>'
                } else { innerHTML += ' | ' }
            }
        }
        innerHTML += `<br>
    New value: <input class="sub_item" type="number" name="value" 
    style="border:solid 1px #3a47d5; position: absolute; left: 170px"><br><br>Reson for change: <textarea class="sub_item" name="reason_for_change" id="" cols="22" rows="2"
    style="border:solid 1px #3a47d5; position: absolute; left: 170px"></textarea><br><br>
    <input class="btn btn-primary" onclick="update_data('/NHSN/Audit/UpdateData','sub_item', '${item_id}')" type="submit" id="Submit"
        name="submit"></input></div>`
        var x = document.getElementById('popup-inside')
        x.innerHTML = innerHTML
    }

}

function closePopup() {
    document.getElementById("popup-1").classList.toggle("active");
}

function update_data(_submit_link, _class_name, item_id) {
    var orig = document.getElementById(item_id)
    var data = orig.dataset
    // console.log(data)
    var cl = document.getElementsByClassName(_class_name)
    for (var j = 0; j < cl.length; j++) {
        data[cl[j].name] = cl[j].value
    }
    // console.log(data)
    fetch(_submit_link, {
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(data)
    }).then(function (response) {
        return response.text();
    }).then(function (text) {
        console.log('Flask reponse:');
        console.log(text);
        location.reload();
    })
}