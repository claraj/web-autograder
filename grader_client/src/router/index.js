import Vue from 'vue'
import Router from 'vue-router'
import Students from '@/components/Students'
import Assignments from '@/components/Assignments'
import Classes from '@/components/Classes'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/students',
      name: 'Students',
      component: Students
    },
    {
      path: '/assignments',
      name: 'Assignments',
      component: Assignments
    },
    {
      path: '/classes',
      name: 'Classes',
      component: Classes
    },

  ]
})
