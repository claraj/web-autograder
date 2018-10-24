import Vue from 'vue'
import Router from 'vue-router'
import Students from '@/components/students/Students'
import Assignments from '@/components/assignments/Assignments'
import ProgrammingClasses from '@/components/classes/ProgrammingClasses'
import GraderResults from '@/components/grades/GraderResults'
import GraderLaunch from '@/components/grades/GraderLaunch'
import GradingBatches from '@/components/grades/GradingBatches'
import StudentDetail from '@/components/students/StudentDetail'
import AssignmentDetail from '@/components/assignments/AssignmentDetail'


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
      path: '/graderlaunch',
      name: 'GraderLaunch',
      component: GraderLaunch
    },
    {
      // All the results from one grading batch
      path: '/graderresults',
      name: 'GraderResults',
      component: GraderResults
    },
    {
      // List of grading batches
      path: '/gradingbatches',
      name: 'GraderBatches',
      component: GradingBatches
    },
    {
      path: '/grader-results/:id',
      name: 'GraderResults',
      component: GraderResults
    },
    {
      path: '/student-detail/:id',
      name: 'StudentDetail',
      component: StudentDetail
    },
    {
      path: '/assignment-detail/:id',
      name: 'AssigmentDetail',
      component: AssignmentDetail
    }



  ]
})
