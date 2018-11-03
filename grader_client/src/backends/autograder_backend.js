import axios from 'axios'
import Vue from 'vue'

function Autograder () {
  this.$api = axios.create({
    baseURL: '/autograder',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': Vue.cookie.get('csrftoken')
    }
  })
}

Autograder.prototype.$invoke = function (data) {
  return this.$api.post(`/grader/`, data)
    .then(response => response.data)
}

Autograder.prototype.$progress = function (batch) {
  return this.$api.get(`/progress/`, {params: {batch: batch}})
    .then(response => response.data)
}

Autograder.prototype.$regrade = function (id) {
  return this.$api.post(`/regrade/`, {id: id})
    .then(response => response.data)
}

Autograder.prototype.$textReport = function (id) {
  return this.$api.get(`/text/${id}`)
    .then(response => response.data)
}

export default Autograder
