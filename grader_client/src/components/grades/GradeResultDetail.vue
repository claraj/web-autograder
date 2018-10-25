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

    <p>Grade: {{ report.total_points_earned }} out of {{ report.total_points_available }}</p>
    <!-- <P>Generated Report {{result.generated_report}}</p> -->
    <!-- <GeneratedGradeReport v-bind:report="result.generated_report"></GeneratedGradeReport> -->


    <!-- List of questions here

    question number; code file; list of tests; points avail;  tests passed/failed; points earned; instructor comments; instructor adjust grade
  -->

  <p v-for="qr in report.question_reports">

    <!-- <P>question report: {{qr}}</p> -->
      <ul>
        <p>question: {{qr.question.question}}</p>

        <p>points avail: {{qr.points_available}}</p>
        <p>source file: {{qr.source_file}}</p>
        <p>test files:
          <ul><li v-for="f in qr.question.test_files"> {{f}} </li></ul>
        </p>

        <!-- <p>report files: {{qr.report_files}}</p> -->

        <p>No. tests {{qr.tests}}</p>
        <p>No. passes {{qr.passes}}</p>

        <p>test suites<p>
          <ul><li v-for="tss in qr.testsuites">
             {{tss.name}} Tests {{tss.tests}} Fails {{tss.failures}} Errors {{tss.errors}} Passes {{tss.passes}}

            <ul><li v-for="ts in tss.testsuites">
               {{ts.name}} Tests {{ts.tests}} Fails {{ts.failures}} Errors {{ts.errors}} Passes {{ts.passes}}

              <ul><li v-for="tc in ts.testcases">
                {{tc.name}} Passed? {{tc.passed}}
                  <p v-if="tc.error">Errored {{tc.error.message}} {{tc.error.fulltext}}</p>
                  <p v-if="tc.failure">Failed {{tc.failure.message}} {{tc.failure.fulltext}}</p>

                {{tc.message}} {{tc.fulltext}}
              </li></ul>


            </li></ul>


          </li></ul>

        <p>Points earned {{qr.points_earned}}</p>






        <p>Instructor comments<input /></p>
        <p>Adjusted points<input /></p>
      </ul>
    </p>



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
      console.log('The grade report is ', this.report)

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
