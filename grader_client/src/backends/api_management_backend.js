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

Backend.prototype.$fetchItems = function() {
  return this.$crud.get(`/${this.base}/`)
  .then(response => response.data)
}

// TODO fix these names.
Backend.prototype.$editItem = function (data)  {
  return this.$crud.patch(`/${this.base}/${data.id}/`, data)
  .then(response => console.log('backend edit', response))
}

Backend.prototype.$deleteItem = function (id) {
  return this.$crud.delete(`/${this.base}/${id}/`,)
  .then(response => response.data)
}

Backend.prototype.$addItem = function(data)  {
  return this.$crud.post(`/${this.base}/`, data)
  .then(response => response.data)
}

Backend.prototype.$fetchOne = function(id) {
  return this.$crud.get(`/${this.base}/${id}/`)
  .then( response => response.data )
}


Backend.prototype.$query = function(query)  {
  return this.$crud.get(`/${this.base}`, { params: query } )
  //.then(response => console.log(`backend filter query reponse for ${query}`, response))
//.catch(err=>console.log(err))
}


Backend.prototype.$bulkAdd = function(data) {
  console.log('backend raw data:', data)
  return this.$bulk.post(
    `/${this.base}s/raw/`,     // YUCK YUCK YUCK FIXME
    data
  )
  .then(response => response.data)
  .catch(err => console.error(err))
}



export default Backend
