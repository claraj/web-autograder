import axios from 'axios'
import Vue from 'vue'

function Autograder() {
  // todo !
  this.$api = axios.create({
    headers: {
      baseURL: '/autograder',
      headers: {
        'Content-Type': 'application/json',
        "X-CSRFToken": Vue.cookie.get("csrftoken")
      }
    }
  })
}

Autograder.prototype.$invokeGrader = function(data) {
  return this.$api.post(``)
  .then(response => console.log('autograder invoke response', response))
}

export default Autograder
