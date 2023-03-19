import Head from 'next/head'
import Image from 'next/image'
import { Inter } from 'next/font/google'
import styles from '@/styles/Home.module.css'
import { useState, useEffect } from 'react'
import { getMovies1, getMovies2 } from './requests'


const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  const [movies1, setMovies1] = useState([])
  const [movies2, setMovies2] = useState([])
  const [movies3, setMovies3] = useState([])

  useEffect(() => {
    getMovies1().then(data => { console.log(data); return data }).then(data => setMovies1(data))
    getMovies2().then(data => setMovies2(data))
  }, [])
  return (
    <>
      <Head>
        <title>Movies</title>
        <meta name="description" content="Compare movies from different apis" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>

        <div className={styles.description}>
        </div>

        <div className={styles.movie}>
          <h1 className={styles.title}>MoviesDatabase</h1>
          <div>
            {movies1.map((movie: any) => (
              <div key={movie.id}>
                <h3>Title: {movie.title}</h3>
                <p>Year: {movie.year}</p>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.movie}>
          <h1 className={styles.title}>IMDb</h1>
          {movies2.map((movie: any) => (
            <div key={movie.id}>
              <h3>Title: {movie.title}</h3>
              <p>Year: {movie.year}</p>
              <p>Type: {movie.titleType}</p>
              <p>Episodes: {movie.numberOfEpisodes}</p>
            </div>

          ))}
        </div>



      </main>
    </>
  )
}
