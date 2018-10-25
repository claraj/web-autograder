<!-- Detail for one graded assignment for one student.  Instructor will be able to add comments on
individual questions, and for the whole assignment  -->

<template>

  <div id="content">

    <!--
    Make these clickable to student or assigmment page
    Student page should have all student's assignments and scores
    Assignment page should have all student's results
  -->

  <div id="header">
    Grade for
    <span v-if="result.fullAssignmentInfo">Assignment Week {{ result.fullAssignmentInfo.week }}</span>
    <span v-else>(Assignment internal ID: {{ result.assignment }})</span>,

    <span v-if="result.fullStudentInfo">student {{ result.fullStudentInfo.name }}</span>
    <span v-else>(Student internal ID: {{ result.student }})</span>.

    (Grade result ID {{ result.id }})
  </div>

  <div id="report">

  <p><span class="title">Date graded:</span> {{ result.date | moment('ddd MMM YYYY hh:mm a')}}</p>
  <p><span class="title">Student GitHub:</span> <a v-bind:href="result.student_github_url">{{ result.student_github_url}}</a></p>
  <p><span class="title">Grade:</span> {{ report.total_points_earned }} out of {{ report.total_points_available }}</p>
    <!-- <P>Generated Report {{result.generated_report}}</p> -->
    <!-- <GeneratedGradeReport v-bind:report="result.generated_report"></GeneratedGradeReport> -->


    <!-- List of questions here

    question number; code file; list of tests; points avail;  tests passed/failed; points earned; instructor comments; instructor adjust grade
  -->

  <p v-for="qr in report.question_reports">
    <ul>
        <p class="question-header"><span class="title">Question:</span> {{qr.question.question}}</p>
        <p><span class="title">Points avail:</span>  {{qr.points_available}}</p>
        <p><span class="title">Source file:</span>  {{qr.source_file}}</p>
        <p><span class="title">Test files:</span>
          <ul><li v-for="f in qr.question.test_files"> {{f}} </li></ul>
        </p>

        <P><span class="title">Total tests:</span>  {{qr.tests}} </p>
        <P><span class="title">Total test passes:</span> {{qr.passes}}
          <span class="passed" v-if="qr.tests === qr.passes">All passed</span>
          <span class="not-passed" v-else>Fails and/or Errors</span>
         </p>

        <p><span class="title">Test Suites:</span></p>
          <ul><li v-for="tss in qr.testsuites">
             Name: {{tss.name}}, Tests: {{tss.tests}}, Fails: {{tss.failures}}, Errors: {{tss.errors}}, Passes: {{tss.passes}}

            <ul><li v-for="ts in tss.testsuites">
               Name: {{ts.name}}, Tests: {{ts.tests}}, Fails: {{ts.failures}}, Errors: {{ts.errors}}, Passes: {{ts.passes}}

              <ul><li v-for="tc in ts.testcases">
                <span class="testcase-name">{{tc.name}}</span> <span v-if="tc.passed" class="passed">Passed</span>
                  <p v-if="tc.error"><span class="not-passed">Errored</span> {{tc.error.message}} <br> {{tc.error.fulltext}}</p>
                  <p v-if="tc.failure"><span class="not-passed">Failed</span> {{tc.failure.message}} <br> {{tc.failure.fulltext}}</p>
              </li></ul>
            </li></ul>
          </li></ul>

        <p><span class="title">Points earned for question:</span> {{qr.points_earned}}</p>

        <p><span class="title">Instructor comments for question: </span> <textarea v-model="qr.instructor_comments"></textarea></p>
        <p><span class="title">Adjusted points: </span> <input v-model="qr.adjusted_points" /></p>
      </ul>
    </p>

    <P><span class="title">Overall Instructor Comments:</span>
      <textarea id="overall-comments" v-model="report.overall_instructor_comments" v-on:change="updateInstructorComments">
      </textarea></P>

      <p>All looks good?</p> <input type="checkbox" v-model="lgtm" v-on:click="allGood()"/>

    </div>

    <div id="buttons">
    <button id="save">SAVE</button>
    <br>
    <button id="d2l-report">D2L Report</button>
    </div>

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
      report: {},
      lgtm: false,
      backupOverall: ''
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
    // Stringify the whole report and send it back to server
    let stringReport = JSON.Stringify(this.report)
    this.result.report = stringReport
    this.$grade_backend.$editItem(result.id, this.result).then( () => {
      console.log('saved, hopefully. ')
    }
  )

  },
  allGood() {
    console.log(this.lgtm)

    if (!this.lgtm) {
      this.backupOverall = this.result.overall_instructor_comments
      this.report.overall_instructor_comments = "Everything looks good. Thanks!"
    }

    else {
      console.log('backed up:', this.backupOverall)
      this.report.overall_instructor_comments = this.backupOverall  || ''
    }
  }
}
}

</script>

<style>

#content {
  text-align: left;
  padding-left: 0px;
  padding-right: 0px;
}

#header {
  font-size: 20px;
  font-weight: bold;
  text-align: center;
}

.passed {
  color: green;
  font-weight: bold;
}

.not-passed {
  color: red;
  font-weight: bold;
}


#report {
  padding-top: 5px;
}

p {
  margin: 2px;
}

.title {
  font-weight: bold;
}

#overall-comments {
  width: 100%;
}

.testcase-name {
  font-style: italic;
  font-weight: bold;
}

.question-header {
  padding-top: 10px;
  font-size: 20px;
}

#buttons {
  position: fixed;
  top: 0;
  right: 0;
  margin: 100px;
  /* width: 100; */
  height: 50px;
  background-color: orange;
  font-size: 20px;
  padding: 20px;
}

button {
  width: 100px;

}

</style>
