<!-- Detail for one graded assignment for one student.  Instructor will be able to add comments on
individual questions, and for the whole assignment  -->

<template>
  <div id="content">

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

      <div v-if="report.error">

        <p><span class="section-title">Errors</span></P>
          <p><span><span class="title not-passed">Error fetching or running code:</span> {{report.error }}</span></p>
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
                  <span class="warning-message" v-if="qr.adjusted_points < 0 || qr.adjusted_points > report.total_points_available">
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


          <div v-show="showTextReport" id="text-report">
            <p><pre ref="fullReportText" id="full-report-text">{{textReport}}</pre></p>
            <input id="mirror-text-report" :value="textReport"></input>
            <button @click="hideTextReport">Close</button>
            <button @click.stop.prevent="copyText">Copy</button>
            <span v-show="copied">Copied to clipboard</span>
          </div>


        </div>
      </template>

<script>

export default {
  name: "GradeResultDetail",

  data() {
    return {
      result: {},
      report: {},
      lgtm: false,
      backupOverall: '',
      totalAdjustedPoints: 0,
      textReport: '',
      showTextReport: false,
      copied: false
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
  watch: {
    lgtm: function() {
      this.allGood()
    }
  },
  methods: {
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
    copyText() {
      let textHolder = document.querySelector('#mirror-text-report')
      textHolder.select()
      document.execCommand('copy')
        this.copied = true
      let vue = this
      setTimeout( function() {vue.copied = false}, 2000)
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

      console.log('adjusting total for ', this.report)

      if (!this.report.question_reports) {
        return
      }

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

  #text-report {
    position: absolute;
    width: 80%;
    height: 500px;
    z-index: 10;
    top: 50%;
    margin: auto;
    left: 50%;
    /* margin: -100px 0 0 -150px; */
    border: 1px darkgray solid;
    background-color: white;
    transform: translate(-50%, -50%);
    box-shadow: 3px 6px 14px darkgray;
  }

  #text-report p {
    border: 1px darkgray solid;
    overflow: scroll;
    margin: 10px;
    padding: 5px;
    height: 430px;
  }

  #text-report pre {
    white-space: pre-wrap;
  }

  button {
    margin-left: 10px;
  }

  /* Hide input with copy of report in. Can't set visibility = none or size to 0px */
  #mirror-text-report {
    opacity: 0;
    width: 10px;
  }

</style>
