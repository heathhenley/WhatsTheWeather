import React, { useState, useEffect } from 'react';
import { useLoaderData, Await, Navigate} from 'react-router-dom'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form';
import Loading from './Loading';
import './App.css'


const WeatherSummary = (
  {zipcode, role, data, roles}: {zipcode: string, role: string, data: any, roles: string[]}) => {
  const [current_role, setRole]= useState<string>(role);
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
        href={`/weather/${zipcode}/${current_role}`}>
          Regen {zipcode}
      </Button>
      { roles ?
        <div><p>as</p>
          <Form.Group className="mb-3" controlId="role">
            <Form.Select name="role" value={current_role} onChange={(e) => {setRole(e.target.value);}}>
              {roles.map(
                (r: string) => {
                  return <option key={r} value={r}>{r}</option>
                })}
            </Form.Select>
          </Form.Group>
        </div>
      : null }
    </div>
  </div>)
}

function Weather() {
  // TODO: improve typescript-fu enough to fix this type
  const { params, data} = useLoaderData() as any;
  const [roles, setRoles]= useState<string[]>([]);

  // TODO: figure this out with react-router
  // I know this is bad practice, but I'm not sure how to do this correctly the
  // react-router / loader setup
  useEffect(() => {
    fetch('https://whatstheweather-production.up.railway.app/weather/roles')
    .then(res => res.json())
    .then(data => {
      setRoles(data.roles);
    })
    .catch(err => console.log(err));
  }, []);

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
                        roles={roles}
                        {...params}>
                      </WeatherSummary>}
            </Await>
        </React.Suspense>
      </main>
    </div>
  )
}

export default Weather
