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
  return this.$api.post(`/grader`, data)    // what URL?
  .then(response => console.log('autograder invoke response', response))
  //expecting webhook response
}


Autograder.prototype.$pollGrader = function(session) {
  return this.$api.post(`/grader/status`, session)    // what URL?
  .then(response => console.log('autograder invoke response', response))
  //expecting webhook response
}


export default Autograder
