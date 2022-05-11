function display_hash() {
    let entries = document.getElementById('search').value
    if (entries.length >= 3) {
        var request = fetch("/search", {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                value: entries
            })
        })
            .then(response => {
                response.text().then((val) => {
                    let box = document.getElementById('container_search')
                    let overlay = document.getElementById('search')
                    box.classList.toggle('hide')
                    for(var i = 0; i < val.length; i++) {
                        let hash = val[i]
                        let block = document.createElement('div')
                        overlay.append(block)
                        let value = document.createElement('h2')
                        block.append(value)
                        block.className = 'hash_block'
                        value.innerHTML = hash
                    }
                })
            })
            .catch(error => alert("Erreur : " + error));
    }
}

function mine() {
    fetch("http://127.0.0.1:5000/mine_block", {
        method: "GET",
        mode: 'no-cors'
    })
        .then(response => {
            response.text().then((val) => {
                location.reload(true)
            })
        })
        .catch(error => alert("Erreur : " + error));
}

function transaction() {
    fetch("http://127.0.0.1:5000/transactions", {
        method: "GET",
        mode: 'no-cors'
    })
        .then(response => {
            response.text().then((val) => {
            })
        })
        .catch(error => alert("Erreur : " + error));
}
