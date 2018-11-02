// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'

import axios from 'axios'
import VueAxios from 'vue-axios'
import VueMoment from 'vue-moment'

import APIBackend from '@/backends/api_management_backend'
import AutograderBackend from '@/backends/autograder_backend'
import EnrollmentBackend from '@/backends/enrollment_backend'

Vue.use(VueAxios, axios)
Vue.use(VueMoment);


// All vue objects will have access to these objects.
Vue.prototype.$student_backend = new APIBackend('student')
Vue.prototype.$assignment_backend = new APIBackend('assignment')
Vue.prototype.$classes_backend = new APIBackend('programmingclass')
Vue.prototype.$grade_backend = new APIBackend('grade')
Vue.prototype.$gradertask_backend = new APIBackend('gradingbatch')

Vue.prototype.$autograder_backend = new AutograderBackend()

Vue.prototype.$enrollment_backend = new EnrollmentBackend()

let VueCookie = require('vue-cookie')
Vue.use(VueCookie)

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
