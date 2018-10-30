<!-- Results of one grading batch.  -->
<template>
  <div>

      <ThingsGradedList
        v-bind:students="uniqueStudents"
        v-bind:assignments="uniqueAssignments"
        >
      </ThingsGradedList>

      <h3>Results</h3>

      <div v-if="readyResults.length">
        <div v-for="result in sortedResults">
          <GradeResultSummary
            v-bind:result="result"
            @onUpdatedInstructorComments="onUpdatedInstructorComments">
          </GradeResultSummary>
          <hr>
        </div>
      </div>

      <div v-else>
        <p>No results</p>
      </div>
  </div>
</template>

<script>

import GradeResultSummary from './GradeResultSummary'
import ThingsGradedList from './ThingsGradedList'

export default {
  name: "GradeResultsList",
  components: { GradeResultSummary, ThingsGradedList },
  props: {
    readyResults: Array,
  },
  data() {
    return {
      sortedResults: [],
      uniqueStudents: [], // Unique student names
      uniqueAssignments: []
    }
  },
  mounted() {
    console.log('READY=', this.readyResults)
    this.sortedResults = this.sortResults()
  },
  watch: {
    readyResults: {
      handler: function () {

        this.sortedResults = this.sortResults()
        this.updateUnique()

      }, deep: true // Watch nested objects for changes.
    }
  },
  methods: {
    onUpdatedInstructorComments (id, report) {
      this.$emit('onUpdatedInstructorComments', id, report)
    },
    sortResults () {
      let sorted = [...this.readyResults]
      // Sort by assignment and then by student
      sorted.sort( (a, b) => {
        // If same assignment week, sort by student
        if (a.assignment.week === b.assignment.week) {
          return a.student.name.toLowerCase().localeCompare(b.student.name.toLowerCase())
        }
        else {
          // Otherwise, sort by assignment
          return a.student.week - b.assignment.week
        }
      })
      return sorted
    },
    updateUnique () {
      console.log('find unique names/asgnts ', this.results)

      let studentNames = this.sortedResults.map(res => res.student.name)
      this.uniqueStudents = []
      studentNames.forEach( n => {
        if (!this.uniqueStudents.includes(n)) {
          this.uniqueStudents.push(n) }
        })
      this.uniqueStudents.sort()

      let assignmentNames = this.sortedResults.map(res => res.assignment.week)

      console.log(assignmentNames)

      this.uniqueAssignments = []
      assignmentNames.forEach( n => {
        if (!this.uniqueAssignments.includes(n)) {
          this.uniqueAssignments.push(n)
        }
      })
      this.uniqueAssignments.sort()
    }
  }
}

</script>
