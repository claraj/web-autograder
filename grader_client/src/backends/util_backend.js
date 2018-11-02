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

Backend.prototype.$getMostRecentAssignmentForStudent = function (student, programming_class) {
  return this.$crud.get('/grade/latestGrades/', { params: {student, programming_class}} )
    .then(response => response.data)
}

export default Backend
