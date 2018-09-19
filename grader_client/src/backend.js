/* eslint-disable */
import axios from 'axios'

import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)


let $backend = axios.create({
   baseURL: '/api',
   headers: {
    'Content-Type': 'application/json',
    "X-CSRFToken": Vue.cookie.get("csrftoken")
  }
})


let $bulk_backend = axios.create({
   headers: {
    'Content-Type': 'text/plain',
    "X-CSRFToken": Vue.cookie.get("csrftoken")
  }
})

// Response interceptor, for doing the same thing with all errors
$backend.interceptors.response.use(
  function (response) {
    return response
  },
  function (error) {
    console.log(error)
    return Promise.reject(error)
  }
)


$backend.$fetchStudents = () => {
  return $backend.get('/student/')
    .then(response => response.data)
}

$backend.$editStudent = (data) => {
  console.log(data)
  return $backend.patch(`/student/${data.id}/`, data)
    .then(response => console.log(response))
}

$backend.$deleteStudent = (id) => {
  return $backend.delete(`/student/${id}/`,)
    .then(response => console.log(response))
}

$backend.$addStudent = (data) => {
  return $backend.post('/student/', data)
    .then(response => console.log(response))
}


$backend.$fetchAssignments = () => {
  return $backend.get('/assignment/')
    .then(response => response.data)
}

$backend.$editAssignment = (data) => {
  console.log(data)
  return $backend.patch(`/assignment/${data.id}/`, data)
    .then(response => console.log(response))
}

$backend.$deleteAssignment = (id) => {
  return $backend.delete(`/assignment/${id}/`,)
    .then(response => console.log(response))

}

$backend.$addAssignment = (data) => {
  return $backend.post('/assignment/', data)
    .then(response => console.log(response))
}

$bulk_backend.$bulkAddStudent = (data) => {
  console.log('backend raw data:', data)
  return $backend.post(
      '/students/raw/',
      data,

  )
    .then(response => response.data)
    .catch(err => console.error(err))
}


$bulk_backend.$bulkAddAssignment = (data) => {
  console.log('backend raw data:', data)
  return $backend.post(
      '/assignments/raw/',
      data
  )
    .then(response => response.data)
    .catch(err => console.error(err))
}


export default { $backend, $bulk_backend }
