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
      name: 'students',
      component: Students
    },
    {
      path: '/assignments',
      name: 'assignments',
      component: Assignments
    },
    {
      path: '/classes',
      name: 'programming-classes',
      component: ProgrammingClasses
    },
    {
      path: '/graderlaunch',
      name: 'grader-launch',
      component: GraderLaunch
    },
    {
      // All the results from one grading batch
      path: '/graderresults',
      name: 'grader-results',
      component: GraderResults
    },
    {
      // List of grading batches
      path: '/gradingbatches',
      name: 'grading-batches',
      component: GradingBatches
    },
    {
      path: '/grader-results/',
      name: 'grader-results',
      component: GraderResults
    },
    {
      path: '/student-detail/:id',
      name: 'student-detail',
      component: StudentDetail
    },
    {
      path: '/assignment-detail/:id',
      name: 'assigment-detail',
      component: AssignmentDetail
    }
  ]
})
