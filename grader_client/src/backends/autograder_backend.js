import axios from 'axios'
import Vue from 'vue'

function Autograder() {
  // todo !
  this.$api = axios.create({
    baseURL: '/autograder',
    headers: {
      'Content-Type': 'application/json',
      "X-CSRFToken": Vue.cookie.get("csrftoken")
    }

  })
}

Autograder.prototype.$invokeGrader = function(data) {
  console.log('sending data:', data)
  return this.$api.post(`/grader/`, data)    // what URL?
  .then(response => response.data)
  //expecting webhook response
}


Autograder.prototype.$pollGrader = function(batch) {
  return this.$api.get(`/progress/`, { batch })    // what URL?
  .then(response => response.data)
  //expecting webhook response
}


export default Autograder
