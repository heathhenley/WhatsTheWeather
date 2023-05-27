//import viteLogo from '/vite.svg'
import { useLoaderData, Navigate} from 'react-router-dom'
import { useState } from 'react'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import './App.css'

function App() {
  const roles = useLoaderData() as string[];
  const [zipcode, setZipcode] = useState<string>('');
  const [role, setRole] = useState<string>('');

  const fetchWeather = (e: React.FormEvent) => {
    e.preventDefault();
    const target = e.currentTarget as typeof e.currentTarget & {
      zipcode: { value: string };
      role: { value: string };
    };
    setZipcode(target.zipcode.value);
    setRole(target.role.value);
  }
  
  
  return (
    <div className="App">
      <header className="App-header">
        <h1>What's the weather?</h1>
      </header>
      <main>
        {(role && zipcode) ? <Navigate to={`/weather/${zipcode}/${role}`} /> : null}
        <div className="weatherInput">
          <Form className="zipcodeInput"
                onSubmit={(e)=>fetchWeather(e)}>
            <Form.Group className="mb-3">
              <Form.Label htmlFor="zipcode">Enter your US zipcode</Form.Label>
              <Form.Control name="zipcode" type="text" placeholder="Enter your US zipcode" maxLength={5} required></Form.Control>
            </Form.Group>
            <Form.Group className="mb-3" controlId="role">
              <Form.Select name="role">
               {roles.map(
                 (role: string) => {
                   return <option key={role} value={role}>{role}</option>
                 })}
              </Form.Select>
            </Form.Group>
            <Button type="submit">Search</Button>
          </Form>
        </div>
      </main>
    </div>
  )
}

export default App
