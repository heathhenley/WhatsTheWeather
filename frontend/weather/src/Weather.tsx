import React from 'react';
import { useLoaderData, Await, Navigate} from 'react-router-dom'
import Button from 'react-bootstrap/Button'
import Loading from './Loading';
import './App.css'

const WeatherSummary = ({zipcode, role, data}) => {
  return (
  <div className="weatherSummaryContainer">
    <div className="weatherSummary">
      <p>{data.summarized_weather}</p>
      <Button
        variant="secondary"
        href="/">
        New Search
      </Button>
      <Button
        variant="primary"
        href={`/weather/${zipcode}/${role}`}>
          Regen {zipcode}
      </Button>
    </div>
  </div>)
}

function Weather() {
  // TODO: improve typescript-fu enought to fix this type
  const { params, data } = useLoaderData() as any;

  return (
    <div className="App">
      <header className="App-header">
        <h1>What's the weather?</h1>
      </header>
      <main>
        <React.Suspense fallback={<Loading />}>
            <Await resolve={data} errorElement={<p>Error</p>}>
              {(d) => <WeatherSummary
                        data={d}
                        zipcode={params.zipcode}
                        role={params.role}>
                      </WeatherSummary>}
            </Await>
        </React.Suspense>
      </main>
    </div>
  )
}

export default Weather
