// alert('Yes it is linked')

const choice = document.querySelector('#press')
const gallery = document.querySelector('#frame')
const complex = document.querySelector('#addLike')

function addText(event){
    event.preventDefault()


}

function randomPraise(event){
    event.preventDefault()
    fetch("api/random_praise")
        .then(res=> res.json() )
        .then(data=> {
            gallery.innerText= data['sun']
            console.log(data)
            complex.href = "/api/like/" + data['id'] + "/praise"
        })
    //     .catch(err => console.log(err))
    // gallery.innerText = 'thing'
    // return gallery
}


function randomShame(event){
    event.preventDefault()
    fetch("api/random_shame")
        .then(res=> res.json() )
        .then(data=> {
            gallery.innerText= data['shade']
            console.log(data)
            complex.href = "/api/like/" + data['id'] + "/shame"
        })
    }