<!-- Detail for one graded assignment for one student.  Instructor will be able to add comments on
individual questions, and for the whole assignment  -->

<template>

  <div>

    <!--
    Make these clickable to student or assigmment page
    Student page should have all student's assignments and scores
    Assignment page should have all student's results
    -->

    <h4>Result ID {{ result.id }}</h4>

    <P v-if="result.fullAssignmentInfo">Assignment Week: {{ result.fullAssignmentInfo.week }}</P>
    <P v-else>Assignment internal ID: {{ result.assignment }}</P>

    <p v-if="result.fullStudentInfo">Student Name: {{ result.fullStudentInfo.name }}</p>
    <P v-else>Student internal ID: {{ result.student }}</P>

    <P>Date graded: {{ result.date | moment('ddd MMM YYYY hh:mm a')}}</p>

    <p>Grade: {{ result.score }}</p>
    <!-- <P>Generated Report {{result.generated_report}}</p> -->
    <!-- <GeneratedGradeReport v-bind:report="result.generated_report"></GeneratedGradeReport> -->


    <!-- List of questions here

    question number; code file; list of tests; points avail;  tests passed/failed; points earned; instructor comments; instructor adjust grade
    -->


    <P>Overall Instructor Comments <textarea v-model="result.instructor_comments" v-on:change="updateInstructorComments"></textarea></P>
    <P>Student GitHub <a v-bind:href="result.student_github_url">{{ result.student_github_url}}</a></p>
  </div>

</template>

<script>

import GeneratedGradeReport from './GeneratedGradeReport'

export default {
  name: "GradeResultDetail",
  components: { GeneratedGradeReport },
  data() {
    return {
      result: {},
      report: {}
    }
  },
  mounted() {

    console.log('my object is', this.result)

    let id = this.$route.query.id
    this.$grade_backend.$fetchOne(id).then(data => {
      this.result = data
      return this.$assignment_backend.$fetchOne(this.result.assignment)
    }).then( (asgt) => {
      //fetch student info, fetch assignment info
      this.result.fullAssignmentInfo = asgt
      return this.$student_backend.$fetchOne(this.result.student)
    }).then(student => {
      this.result.fullStudentInfo = student

      console.log('all data fetched', this.result)

      this.report = JSON.parse(this.result.generated_report)
      console.log(this.report)

    }).catch( err => {
      console.log('errrrr', err)
    })
},

methods: {
  updateInstructorComments() {
    // TODO
  }
}
}

</script>
