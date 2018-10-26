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

  <div v-if="report.error">

    <p><span class="section-title">Errors</span></P>
    <p><span class="warning"><span class="title">Error fetching or running code:</span> {{report.error }}</span></p>
  </div>

  <div v-else>

  <p><span class="title">Calculated grade:</span> {{ report.total_points_earned | toFixed(2) }} out of {{ report.total_points_available }}</p>

  <p v-for="qr in report.question_reports">
    <ul id="why">
        <p class="question-header"><span class="title">Question:</span> {{qr.question.question}}</p>
        <p><span class="title">Points available:</span>  {{qr.points_available}}</p>
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
             <span class="testsuite-name">{{tss.name}}:</span> {{tss.tests}} Tests, {{tss.failures}} Fails, {{tss.errors}} Errors, {{tss.passes}} Passes.

            <ul><li v-for="ts in tss.testsuites">
               <span class="testsuite-name">{{ts.name}}:</span> {{ts.tests}} Tests, {{ts.failures}} Fails, {{ts.errors}} Errors, {{ts.passes}} Passes.

              <ul><li v-for="tc in ts.testcases">
                <span class="testcase-name">{{tc.name}}</span> <span v-if="tc.passed" class="passed">Passed</span>
                  <p v-if="tc.error"><span class="not-passed">Errored</span> {{tc.error.message}} <br> {{tc.error.fulltext}}</p>
                  <p v-if="tc.failure"><span class="not-passed">Failed</span> {{tc.failure.message}} <br> {{tc.failure.fulltext}}</p>
              </li></ul>
            </li></ul>
          </li></ul>

        <p><span class="title">Points earned for question:</span> {{qr.points_earned | toFixed(2) }}</p>

        <p><span class="title">Instructor comments for question <span>{{qr.question.question}}</span>: </span> <textarea class="question-comments" v-model="qr.instructor_comments" v-on:change="updateQuestionComments()"></textarea></p>
        <p><span class="title">Adjusted points: </span> <input v-on:change="updateAdjustedPoints(qr.adjusted_points)" v-model="qr.adjusted_points" />
          <span class="warning" v-if="qr.adjusted_points < 0 || qr.adjusted_points > report.total_points_available">
            Adjusted points not valid
          </span>
        </p>
      </ul>
    </p>
  </div>


    <div>
    <p class="section-title">Summary</p>

    <p><span class="title">Calculated grade:</span> {{ report.total_points_earned | toFixed(2) }} out of {{ report.total_points_available }}</p>
    <p><span class="title">Total adjusted points: </span>{{totalAdjustedPoints | toFixed(2) }} out of {{ report.total_points_available }}
      <span class="warning" v-if="totalAdjustedPoints < 0 || totalAdjustedPoints > report.total_points_available">
        Adjusted points not valid
      </span>
    </p>

    <P><span class="title">Overall Instructor Comments:</span>
      <textarea id="overall-comments" v-model="report.overall_instructor_comments" v-on:change="updateOverallInstructorComments">
      </textarea></P>

      <p>All looks good? <input type="checkbox" v-model="lgtm" v-on:click="allGood()"/></p>

    </div>
    </div>

    <div id="buttons">
    <button id="save" v-on:click="save()">SAVE</button>
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
      backupOverall: '',
      totalAdjustedPoints: 0
    }
  },
  filters: {
    toFixed: function(value, decimal_places) {
      if (value && !isNaN(value)) {
        return value.toFixed(decimal_places)
      }
      return value
    }
  },
  mounted() {

    console.log('my result object is', this.result)

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

      this.updateTotalAdjustedPoints()

    }).catch( err => {
      console.log('errrrr', err)
    })
},

methods: {

  save() {

    console.log('save', this.result.id)
    let stringReport = JSON.stringify(this.report)
    this.result.generated_report = stringReport
    this.$grade_backend.$editItem(this.result).then( () => {
      console.log('saved, hopefully. ')
    })
  },
  updateQuestionComments(comment) {
    this.save();
  },
  updateOverallInstructorComments(comment) {
    // Stringify the whole report and send it back to server
    // TODO waqqAQvalidationq`1 here if needed
    this.save()
  },

  updateAdjustedPoints(pts) {
    // TODO validation, is number, no negative points
      if (isNaN(pts)) {
        alert('numbers only!')
        return
      }

      if (pts < 0) {
        alert('positive numbers please')
      }

      //update total adjusted

      this.updateTotalAdjustedPoints()

      this.save()
  },

  updateTotalAdjustedPoints() {

    console.log('adjusting total for ', this.report)

    this.report.question_reports.forEach( q => {
      if (!q.adjusted_points) {
        q.adjusted_points = q.points_earned.toFixed(2)
      }
    })


    let sum = this.report.question_reports.reduce( (s, q) => {
      console.log(s, q.adjusted_points)
      return Number(s.adjusted_points) + Number(q.adjusted_points)
    })

    this.totalAdjustedPoints = sum


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

<style scoped>  /* otherwise all the other components will get these styles . */

#why {
  padding-left: 0px;
}

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

.section-title {
  font-size: 20px;
  font-weight: bold;
}

#overall-comments {
  width: 100%;
}

.question-comments {
    width: 100%;
}


.testcase-name {
  font-style: italic;
  font-weight: bold;
}

.testsuite-name {
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
  margin: 30px;
  /* width: 100; */
  height: 50px;
  background-color: orange;
  font-size: 20px;
  padding: 20px;
}

button {
  width: 100px;
}

.warning {
  font-style: italic;
  font-weight: bold;
  color: darkred;
}



</style>
