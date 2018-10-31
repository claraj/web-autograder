
<template>

  <div>

     <h2>{{student.name}}</h2>

     <p>Name: {{ student.name}} </p>
     <p>GitHub: {{ student.github_id}} </p>
     <p>Star ID: {{ student.star_id}} </p>
     <p>Org ID: {{ student.org_id}} </p>

     <P>Programming classes: {{student.programming_classes}}</p>

     <h2>Grades</h2>

      <p>TODO fetch the lastest grades for this student. </p>

<h3>Grades</h3>

<div v-for="gradeSet in latestGrades">
<GradeSummarySetHolder
  v-bind:grades="gradeSet"
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
      latestGrades: [

      ],
      dogs: [
          {dog : { borks: [1, 2, 3] }} ,
          {dog: { borks: [5,62, 7]}} ,
      ]
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
        let proms = student.programming_classes.map(pc => {return vue.$student_backend.$temp_latest_asgt_for_student(student.id, pc)})
        let latestGrades = await Promise.all(proms) //.then( vals => vue.latestGrades = vals)  // aparently I don't understand await.

        console.log('latest', latestGrades)
        return latestGrades
      }

      getStudent().then( (grades) => {
        vue.latestGrades = grades
      })
  },

  onRegrade(id) {
    // fire grader for this
    console.log('DETAILL REGRADE ' , id)
    this.$autograder_backend.$regrade(id)
    .then(response => {
      this.$router.push({name: 'grader-results', query: {id: response.batch, expectedResults: 1}})
    })
    .catch(err => console.log(err))


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
