/* eslint-disable */
import axios from 'axios'

import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)

function Backend() {

  this.$crud = axios.create({
    baseURL: '/api',
    headers: {
      'Content-Type': 'application/json',
      "X-CSRFToken": Vue.cookie.get("csrftoken")
    }
  })

  this.$bulk = axios.create({
    headers: {
      'Content-Type': 'text/plain',
      "X-CSRFToken": Vue.cookie.get("csrftoken")
    }
  })

}

Backend.prototype.$fetchProgrammingClassStudents = function(classId) {
  return this.$crud.get(`/programmingclass/${classId}/students/`)
    .then( response => response.data )
}

Backend.prototype.$fetchProgrammingClassAssignments = function(classId) {
  return this.$crud.get(`/programmingclass/${classId}/assignments/`)
    .then( response => response.data )
}

Backend.prototype.$addStudentsToProgrammingClass = function(classId, studentIds) {
  return this.$crud.post(`/programmingclass/${classId}/students/`, {studentIds})
    .then( response => response.data)
}

Backend.prototype.$addAssignmentsToProgrammingClass = function(classId, assignmentIds) {
  return this.$crud.post(`/programmingclass/${classId}/assignments/`, {assignmentIds})
    .then( response => response.data)
}

Backend.prototype.$removeStudentsFromProgrammingClass = function(classId, studentIds) {
  return this.$crud.patch(`/programmingclass/${classId}/students/`, {studentIds})
    .then( response => response.data)
}

Backend.prototype.$removeAssignmentsFromProgrammingClass = function(classId, assignmentIds) {
  return this.$crud.patch(`/programmingclass/${classId}/assignments/`, {assignmentIds})
    .then( response => response.data)
}

export default Backend
