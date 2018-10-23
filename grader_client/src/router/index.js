import Vue from 'vue'
import Router from 'vue-router'
import Students from '@/components/Students'
import Assignments from '@/components/Assignments'
import ProgrammingClasses from '@/components/ProgrammingClasses'
import GraderModules from '@/components/GraderModules'
import GraderResults from '@/components/GraderResults'
import GraderLaunch from '@/components/GraderLaunch'
import GraderTasks from '@/components/GraderTasks'

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
      name: 'ProgrammingClasses',
      component: ProgrammingClasses
    },
    {
      path: '/gradermodules',
      name: 'GraderModules',
      component: GraderModules
    },
    {
      path: '/graderlaunch',
      name: 'GraderLaunch',
      component: GraderLaunch
    },
    {
      path: '/graderresults',
      name: 'GraderResults',
      component: GraderResults
    },
    {
      path: '/gradertasks',
      name: 'GraderTasks',
      component: GraderTasks
    }



  ]
})
