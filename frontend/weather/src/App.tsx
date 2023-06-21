import {
  useLoaderData,
  Outlet,
  Form,
  redirect,
  useLocation,
  useNavigation } from 'react-router-dom'
import Button from 'react-bootstrap/Button'
import { Form as BSForm } from 'react-bootstrap';
import Loading from './Loading';
import './App.css'


interface SearchFormProps {
  roles: string[];
  currentRole?: string;
  currentZipcode?: string;
}

export async function action({ request }: any) {
  const formData =  await request.formData();
  const updates = Object.fromEntries(formData);
  return redirect(`/weather/${updates.zipcode}/${updates.role}`);
}

const SearchForm = ({roles, currentRole, currentZipcode} : SearchFormProps) => {
  return (
    <div className="weatherSearchFrom">
      <BSForm as={Form} method="POST" id="search" >
        <BSForm.Control
          name="zipcode"
          type="number"
          placeholder="US Zipcode"
          maxLength={5}
          required
          defaultValue={currentZipcode ? currentZipcode : 90210} />
        <BSForm.Select
          name="role"
          required
          defaultValue={currentRole ? currentRole : "default"}>
          {
            roles.map((role) => (
              <option key={role} value={role}>
                {role}
              </option>))
          }
        </BSForm.Select>
        <Button type="submit">
          Go
        </Button>
      </BSForm>
    </div>
  )
}

export const App = () => {

  const roles = useLoaderData() as string[];
  const navigation = useNavigation();
  const currentPath = useLocation()?.pathname?.split('/');
  
  const currentRole = (currentPath?.length > 3 ) ? currentPath[3] : undefined;
  const currentZipcode = (currentPath?.length > 3 ) ? currentPath[2] : undefined;

  return (
    <div className="App">
      <header className="App-header">
        <h1>What's the weather?</h1>
      </header>
      <main>
        <div className="weatherInput">
          <SearchForm
            roles={roles}
            currentRole={currentRole}
            currentZipcode={currentZipcode}
          />
        </div>
        <div className="weatherSummaryContainer">
          <div className="weatherSummary">
            {navigation.state === "loading" ? <Loading /> : <Outlet />}
          </div>
        </div>
      </main>
    </div>
  )
}

