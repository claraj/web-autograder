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

}


Autograder.prototype.$graderProgress = function(batch) {
  return this.$api.get(`/progress/`, { params: { batch: batch } } )    // what URL?
  .then(response => response.data)

}


Autograder.prototype.$regrade = function(id) {
  return this.$api.post(`/regrade/`, {id: id} )
  .then(response => response.data)
}


export default Autograder
