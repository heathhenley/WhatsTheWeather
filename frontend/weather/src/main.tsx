import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider, defer } from 'react-router-dom'
import ErrorPage from './ErrorPage'
import Weather from './Weather'
import App from './App'
import './index.css'

async function roleLoader() {
  let roles;
  await fetch('https://whatstheweather-production.up.railway.app/weather/roles')
    .then(res => res.json())
    .then(data => {
      roles = data.roles;
    })
    .catch(err => console.log(err));
  return roles;
}

async function weatherLoader(
  {params} : any) {
  const data = fetch(
    `https://whatstheweather-production.up.railway.app/weather?zipcode=${params.zipcode}&role=${params.role}`).then(res => res.json());
  return defer({ params, data });
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <ErrorPage />,
    loader: roleLoader,
  },
  {
    path: '/weather/:zipcode/:role',
    element: <Weather />,
    errorElement: <ErrorPage />,
    loader: weatherLoader,
  }
]);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
