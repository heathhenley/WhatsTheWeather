//import viteLogo from '/vite.svg'
import React from 'react';
import { useLoaderData, Await } from 'react-router-dom'
import Loading from './Loading';
import './App.css'

function Weather() {
  const { data } = useLoaderData();

  return (
    <div className="App">
      <header className="App-header">
        <h1>What's the weather?</h1>
      </header>
      <main>
        <React.Suspense fallback={<Loading />}>
            <Await resolve={data} errorElement={<p>Error</p>}>
              {(d) => <div className="weatherSummary"><p>{d.summarized_weather}</p></div>}
            </Await>
        </React.Suspense>
      </main>
    </div>
  )
}

export default Weather
