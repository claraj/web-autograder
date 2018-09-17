/* eslint-disable */
import axios from 'axios'

import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)



let $backend = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    "X-CSRFToken": Vue.cookie.get("csrftoken")}
})

$backend.$fetchStudents = () => {
  return $backend.get('student/')
    .then(response => response.data)
}

$backend.$editStudent = (data) => {
  return $backend.put('student/', data)
    .then(response => console.log(response))
}

$backend.$deleteStudent = (id) => {
  return $backend.delete(`student/${id}`,)
    .then(response => console.log(response))

}

$backend.$addStudent = (data) => {
  return $backend.post('student/', data)
    .then(response => console.log(response))
}

export default $backend
