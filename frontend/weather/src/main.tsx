import React from 'react'
import ReactDOM from 'react-dom/client'
import {
  createBrowserRouter,
  RouterProvider } from 'react-router-dom'
import { inject } from '@vercel/analytics'
import ErrorPage from './ErrorPage'
import {WeatherSummary, WeatherSummaryResults} from './WeatherSummary'
import {App, action as searchAction} from './App'
import './index.css'

inject();

const apiUrl = 'https://whatstheweather-production.up.railway.app';

async function roleLoader() : Promise<string[]> {
  let roles : string[] = [];
  await fetch('https://whatstheweather-production.up.railway.app/weather/roles')
    .then(res => res.json())
    .then(data => {
      roles = data.roles;
    })
    .catch(err => console.log(err));
  return roles;
}

/*interface WeatherSummaryLoaderParams {
  params: {
    zipcode: string;
    role: string;
  }
}*/

async function weatherLoader({params}: any) : Promise<WeatherSummaryResults> {
  const data = await fetch(
    `${apiUrl}/weather?zipcode=${params.zipcode}&role=${params.role}`)
    .then(res => res.json());
  return {...params, ...data};
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    errorElement: <ErrorPage />,
    loader: roleLoader,
    action: searchAction,
    children: [
      {
        path: 'weather/:zipcode/:role',
        element: <WeatherSummary />,
        errorElement: <ErrorPage />,
        loader: weatherLoader,
      }
    ],
  },
]);

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
