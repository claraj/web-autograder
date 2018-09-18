import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Students from '@/components/Students'
import Assignments from '@/components/Assignments'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/students',
      name: 'Students',
      component: Students
    },
    {
      path: '/assignments',
      name: 'Assignments',
      component: Assignments
    }
  ]
})
