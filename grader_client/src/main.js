// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import axios from 'axios'
import VueAxios from 'vue-axios'
//import backend from '@/backends/management_backend'

Vue.use(VueAxios, axios)

// All vue objects will have access to these two objects .
// Vue.prototype.$student_backend = backend('student')
// Vue.prototype.$assignment_backend = backend('assignment')
// Vue.prototype.$classes_backend = backend('class')


let VueCookie = require('vue-cookie')
Vue.use(VueCookie)

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
