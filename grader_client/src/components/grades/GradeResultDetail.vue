<!-- Detail for one graded assignment for one student.  Instructor will be able to add comments on
individual questions, and for the whole assignment  -->

<template>
  <div id="content" @click="hideTextReport">

    <div id="header" v-if="result.assignment && result.student">
      Grade for
      <span>Assignment <router-link :to="{ name: 'assignment', params: {id: result.assignment.id } }">Week {{ result.assignment.week }}</router-link>,</span>
      <span>student <router-link :to="{ name: 'student', params:  {id: result.student.id} }">{{ result.student.name }}</router-link></span>
      (Grade result ID {{ result.id }})
    </div>

    <div id="report">

      <p><span class="title">Date graded:</span> {{ result.date | moment('ddd MMM YYYY hh:mm a')}}</p>
      <p><span class="title">Student GitHub:</span> <a v-bind:href="result.student_github_url">{{ result.student_github_url}}</a></p>

      <button class="action-button "@click="regrade">Re-run grader</button>
      <button class="neutral-button "@click="generateTextReport">Generate text report</button>
      <button class="important-button "@click="toggleStackTraces">{{stackTraceAction}} stack traces</button>


      <div v-if="result.ag_error">
        <p><span class="section-title">Errors</span></p>
        <p><span><span class="title not-passed">
          Error when grader tried to fetch or run code:</span>
          {{result.ag_error}}
          <span v-if="result.last_success"><router-link :to="{ name: 'grade-detail', query: {id: result.last_success} }">view here</router-link></span>
          <span v-else>No previous succesful grading runs</span>
        </span></p>
      </div>

      <div v-else>

        <p><span class="title">Calculated grade:</span> {{ report.total_points_earned | toFixed(2) }} out of {{ report.total_points_available }}</p>

        <div v-if="report.error">
          Error in student code: {{report.error}}
          <span v-if="result.last_success"><router-link :to="{ name: 'grade-detail', query: {id: result.last_success} }">view here</router-link></span>
          <span v-else>No previous succesful grading runs</span>
        </div>

        <div v-if="report.question_reports">
        <p v-for="qr in report.question_reports">
          <ul id="why">
            <p class="question-header"><span class="title">Question:</span> {{qr.question.question}}</p>
            <p><span class="title">Points available:</span>  {{qr.points_available}}</p>
            <p><span class="title">Source file:</span>  {{qr.source_file}} <GuessyGitHubFile v-bind:filename="qr.source_file" v-bind:grade="result.id"></GuessyGitHubFile></p>
            <p><span class="title">Test files:</span>
              <ul><li v-for="f in qr.question.test_files"> {{f}}  <GuessyGitHubFile v-bind:filename="f" v-bind:grade="result.id"></GuessyGitHubFile> </li></ul>
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
                  <span v-if="tc.error"><span class="not-passed">Errored</span> {{tc.error.message}} <br> <span class="stack-trace" v-bind:class="{ hidden: stackTraceAction=='Show'}">{{tc.error.fulltext}}</span> </span>
                  <span v-if="tc.failure"><span class="not-passed">Failed</span> {{tc.failure.message}} <br> <span class="stack-trace" v-bind:class="{ hidden: stackTraceAction=='Show'}">{{tc.failure.fulltext}}</span> </span>
                </li></ul>
              </li></ul>
            </li></ul>

            <p><span class="title">Points earned for question:</span> {{qr.points_earned | toFixed(2) }}</p>

            <p><span class="title">Instructor comments for question <span>{{qr.question.question}}</span>: </span> <textarea class="question-comments" v-model="qr.instructor_comments" v-on:change="updateQuestionComments()"></textarea></p>
            <p>
              <span class="title">Adjusted points: </span> <input v-on:change="updateAdjustedPoints(qr.adjusted_points)" v-model="qr.adjusted_points" />
              <span class="warning-message" v-if="qr.adjusted_points < 0 || qr.adjusted_points > report.total_points_available">
              Adjusted points not valid
              </span>
            </p>
          </ul>
        </p>
      </div>
    </div>

      <div>
        <p class="section-title">Summary</p>

        <p><span class="title">Calculated grade:</span> {{ report.total_points_earned | toFixed(2) }} out of {{ report.total_points_available }}</p>
        <p><span class="title">Total adjusted points: </span>{{totalAdjustedPoints | toFixed(2) }} out of {{ report.total_points_available }}
          <span class="warning-message" v-if="totalAdjustedPoints < 0 || totalAdjustedPoints > report.total_points_available">
            Adjusted points not valid
          </span>
        </p>

        <P><span class="title">Overall Instructor Comments:</span>
          <textarea id="overall-comments" v-model="report.overall_instructor_comments" v-on:change="updateOverallInstructorComments">
          </textarea></P>

          <p>All looks good? <input type="checkbox" v-model="lgtm"/></p>

      </div>
    </div>

    <div id="buttons">
      <button id="save" class="important-button" v-on:click="save">Save</button>
      <br>
      <button @click="generateTextReport" id="d2l-report" class="neutral-button">Generate text Report</button>
    </div>

    <GradeTextReport
    v-show="showTextReport" v-bind:text="textReport"
    v-on:hideTextReport="hideTextReport"></GradeTextReport>

  </div>
</template>

<script>

import GradeTextReport from '@/components/grades/GradeTextReport'
import GuessyGitHubFile from '@/components/parts/GuessyGitHubFile'

export default {
  name: "GradeResultDetail",
  components: { GradeTextReport, GuessyGitHubFile },
  data() {
    return {
      result: {},
      report: {},
      lgtm: false,
      backupOverall: '',
      totalAdjustedPoints: 0,
      textReport: '',
      showTextReport: false,
      stackTraceAction: 'Hide'
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
  created() {

  },
  mounted() {
    this.fetchData()
  },
  watch: {
    lgtm: function() {
      this.allGood()
    },
    $route: function() {
      this.fetchData()
    }
  },
  methods: {
    fetchData() {
      let id = this.$route.query.id
      console.log(this.$route.query.id)
      this.$grade_backend.$fetchOne(id)
        .then(data => {
          this.result = data
          console.log('all data fetched', this.result)
          this.report = JSON.parse(this.result.generated_report)
          console.log('The grade report is ', this.report)
          this.updateTotalAdjustedPoints()
        }).catch( err => {
          console.log('Error loading initial data', err)
      })
    },
    save() {
      console.log('save', this.result.id)
      let stringReport = JSON.stringify(this.report)
      this.result.generated_report = stringReport
      this.$grade_backend.$editItem({id: this.result.id, generated_report: stringReport})
      .then( () => {

      })
    },
    regrade () {
      console.log('regrade')
      this.$autograder_backend.$regrade(this.result.id).then(data => {
        // redirect to results page to await result
        console.log('queued')
        this.$router.push({name: 'grader-results', query: {id: data.batch, expectedResults: data.items_to_grade}})
      })
    },
    generateTextReport() {
      this.$autograder_backend.$textReport(this.result.id).then(data => {
        this.textReport = data.text
        this.showTextReport = true
      })
    },
    hideTextReport() {
      this.showTextReport = false
    },
    toggleStackTraces() {
      if (this.stackTraceAction == 'Show') {
        this.stackTraceAction = 'Hide'
      } else {
        this.stackTraceAction = 'Show'
      }
    },
    updateQuestionComments (comment) {
      this.save();
    },
    updateOverallInstructorComments (comment) {
      this.save()
    },
    updateAdjustedPoints (pts) {
      if (isNaN(pts)) {
        alert('Numbers only!')
        return
      }

      if (pts < 0) {
        alert('Positive numbers please')
        return
      }

      this.updateTotalAdjustedPoints()
      this.save()
    },

    updateTotalAdjustedPoints () {

       //console.log('adjusting total for ', this.report)

      if (!this.report.question_reports) {
        this.totalAdjustedPoints = 0
        return
      }

      this.report.question_reports.forEach( q => {
        if (!q.adjusted_points) {
          q.adjusted_points = q.points_earned.toFixed(2)
        }
      })

      let sum = this.report.question_reports.reduce( (s, q) => {
        console.log('summing', s, q.adjusted_points)
        return Number(s) + Number(q.adjusted_points)
      }, 0)

      console.log(sum)
      this.totalAdjustedPoints = sum
    },

    allGood () {
        if (this.lgtm) {
          this.backupOverall = this.report.overall_instructor_comments
          this.report.overall_instructor_comments = "Everything looks good. Thanks!"
        }
        else {
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

  .stack-trace {
    white-space: pre;
  }

  .stack-trace.hidden {
    display: none;
  }


</style>
