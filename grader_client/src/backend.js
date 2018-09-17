import axios from 'axios'

let $backend = axios.create({
  baseURL: '/api',
  headers: {'Content-Type': 'application/json'}
})

$backend.$fetchStudents = () => {
  return $backend.get('student/')
    .then(response => response.data)
}

export default $backend
