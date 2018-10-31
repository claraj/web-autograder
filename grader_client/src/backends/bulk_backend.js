/* eslint-disable */
import axios from 'axios'

import Vue from 'vue'
import VueCookie from 'vue-cookie'
Vue.use(VueCookie)

function Backend(base_url) {

  // constructor(base_url) {
  this.base = base_url

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

Backend.prototype.$bulkAdd = function (data) {
  console.log('backend raw data:', data)
  return this.$bulk.post(
    `/${this.base}/raw/`,     // YUCK YUCK YUCK FIXME
    data
  )
  .then(response => response.data)
  .catch(err => console.error(err))
}



export default Backend
