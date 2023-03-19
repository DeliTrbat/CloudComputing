const getMovies1 = () => {
    return fetch('http://127.0.0.1:5000/mdapi/')
        .then(response => response.json())
        .then(data => data)
}

const getMovies2 = () => {
    return fetch("http://127.0.0.1:5000/imdbapi/")
        .then(response => response.json())
        .then(data => { console.log(data); return data })
        .catch(error => error)
}


export { getMovies1 }
export { getMovies2 }