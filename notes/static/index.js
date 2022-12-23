function deleteTweet(notesID){
    fetch('/delete-tweet',{
        method: 'POST',
        body: JSON.stringify({ notesID })
    }).then((_res) => {
        window.location.href = "/previous-tweets"
    })
}