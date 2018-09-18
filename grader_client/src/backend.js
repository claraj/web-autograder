/* eslint-disable */
import axios from 'axios'

import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)


let $backend = axios.create({
  // baseURL: '/api',
   headers: {
    'Content-Type': 'application/json',
    "X-CSRFToken": Vue.cookie.get("csrftoken")
  }
})

$backend.$fetchStudents = () => {
  return $backend.get('/api/student/')
    .then(response => response.data)
}

$backend.$editStudent = (data) => {
  console.log(data)
  return $backend.patch(`/api/student/${data.id}/`, data)
    .then(response => console.log(response))
}

$backend.$deleteStudent = (id) => {
  return $backend.delete(`/api/student/${id}/`,)
    .then(response => console.log(response))
}

$backend.$addStudent = (data) => {
  return $backend.post('api/student/', data)
    .then(response => console.log(response))
}

$backend.$bulkAdd = (data) => {
  console.log('backend raw data:', data)
  return $backend.post(
      '/students/raw/',
      data,
    {  headers:
      {
        // baseURL: '/',
          'Content-Type': 'text/plain',
        "X-CSRFToken": Vue.cookie.get("csrftoken")
      }
    }
  )
    .then(response => response.data)
    .catch(err => console.error(err))
}


$backend.$fetchAssignments = () => {
  return $backend.get('/api/assignment/')
    .then(response => response.data)
}

$backend.$editAssignment = (data) => {
  console.log(data)
  return $backend.patch(`assignment/${data.id}/`, data)
    .then(response => console.log(response))
}

$backend.$deleteAssignment = (id) => {
  return $backend.delete(`assignment/${id}/`,)
    .then(response => console.log(response))

}

$backend.$addAssignment = (data) => {
  return $backend.post('assignment/', data)
    .then(response => console.log(response))
}

export default $backend
