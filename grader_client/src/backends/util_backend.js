/* eslint-disable */
import axios from 'axios'

import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)

function Backend() {

  this.$api = axios.create({
    baseURL: '/api',
    headers: {
      'Content-Type': 'application/json',
      "X-CSRFToken": Vue.cookie.get("csrftoken")
    }
  })
}

Backend.prototype.$getMostRecentAssignmentForStudent = function (student, programming_class) {
  return this.$api.get('/grade/latestGrades/', { params: {student, programming_class}} )
    .then(response => response.data)
}


Backend.prototype.$studentsInBatch = function(batchId) {
  return this.$api.get(`/gradingbatch/${batchId}/students`)
    .then(response => response.data)
}

Backend.prototype.$assignmentsInBatch = function(batchId) {
  return this.$api.get(`/gradingbatch/${batchId}/assignments`)
    .then(response => response.data)
}
export default Backend
