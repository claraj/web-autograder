
<template>

  <div>

    <h2>{{student.name}}</h2>

    <p>Name: {{ student.name}} </p>
    <p>GitHub: {{ student.github_id}} </p>
    <p>Star ID: {{ student.star_id}} </p>
    <p>Org ID: {{ student.org_id}} </p>

    <P>Programming classes: <span v-for="pc in programmingClasses">{{pc.name}}, {{pc.semester_human_string}}; </span> </p>

      <h2>Grades</h2>

      <div v-if="latestGrades.length > 0" v-for="gradeSet in latestGrades">

        <h4>Grade set for {{gradeSet.programmingClass.name}}, {{gradeSet.programmingClass.semester_human_string}}</h4>

        <button v-on:click="onRegradeAll(gradeSet.programmingClass.id)">Regrade all for {{gradeSet.programmingClass.name}}</button>

        <GradeSummarySetHolder
        v-bind:grades="gradeSet.grades"
        v-bind:programmingClass="gradeSet.programmingClass"
        v-on:onRegrade="onRegrade"
        v-on:onUpdateInstructorComments="onUpdateInstructorComments">
      </GradeSummarySetHolder>
    </div>

  </div>

</template>

<script>

import GradeResultSummary from '@/components/grades/GradeResultSummary.vue'
import GradeSummarySetHolder from '@/components/grades/GradeSummarySetHolder.vue'

export default {
  name: 'StudentDetail',
  components: {GradeResultSummary, GradeSummarySetHolder },
  data() {
    return {
      student: {},
      id: Number,
      latestGrades: [],
      programmingClasses: []
    }
  },
  mounted() {
    this.id = this.$route.params.id
    this.fetchData()
  },
  methods: {
    fetchData () {

      let vue = this
      async function getStudent() {

        let student = await vue.$student_backend.$fetchOne(vue.id)
        vue.student = student

        // TODO how does this work within await, arrow functions?
        let gradeProms = student.programming_classes.map(pc => vue.$util_backend.$getMostRecentAssignmentForStudent(student.id, pc))
        let latestGrades = await Promise.all(gradeProms) //.then( vals => vue.latestGrades = vals)  // aparently I don't understand await.

        let classesProms = student.programming_classes.map(pc => vue.$classes_backend.$fetchOne(pc))
        let programmingClasses = await Promise.all(classesProms)

        console.log('latest', latestGrades)
        return { latestGrades, programmingClasses }
      }

      getStudent().then( (data) => {

        // Make Array of { programmingClass: {...}, grades: [ {...}, {..}.... ]}

        console.log('data',data)

        let programmingClassesArrays = data.programmingClasses

        this.programmingClasses = programmingClassesArrays

        let gradesArray = data.latestGrades
        console.log('pca', programmingClassesArrays)
        console.log('ga', gradesArray)

        let grades = programmingClassesArrays.map(pc => { return { programmingClass: pc }})
        console.log('grades', grades)


        grades.forEach( (g, index) => {
          console.log(g, index)
          g.grades = gradesArray[index]}
        )

        console.log('fin grades', grades)

        this.latestGrades = grades

      })
    },

    onRegrade(id) {
      // fire grader and redirect to expected results page
      this.$autograder_backend.$regrade(id)
      .then(response => {
        this.$router.push({name: 'grader-results', query: {id: response.batch, expectedResults: 1}})
      })
      .catch(err => console.log(err))
    },

    onRegradeAll(classId) {
      // Grade all of the assignments for this class, regardless if they are already graded or not.
      let assignments = this.$enrollment_backend.$fetchProgrammingClassAssignments(classId).then(assignments => {
        let data = { students: [this.student.id], assignments: assignments.map(a => a.id), programming_class: classId}
        console.log('data', data)
        this.$autograder_backend.$invoke(data)
        .then(response => {
          this.$router.push({name: 'grader-results', query: {id: response.batch, expectedResults: assignments.length}})
        })
      })
    },
    onUpdateInstructorComments(id, report) {
      // console.log('DETAIL update', id, report)
      this.$grade_backend.$editItem({id: id, generated_report: report } )
      .then( d => console.log(d))
      .catch(err => console.log(err))
    }
  }
}


</script>
