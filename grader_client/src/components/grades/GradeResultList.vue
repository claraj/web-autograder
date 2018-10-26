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
      studentCache: [],   // readyResults only has the student's ID, this is for full student info objects
      assignmentCache: [],  // as above, for assignments
      uniqueStudents: [], // Unique student names
      uniqueAssignments: []
    }
  },
  mounted() {
    this.fetchDetails()     // For any ready results, fetch the full student and assignment info.
    this.sortedResults = this.sortResults()
  },

  watch: {
    readyResults: {
      handler: function () {
        // fetch student info, fetch assignment info
        // what's the new result?
        console.log('READY RESULTS CHANGED')
        this.fetchDetails(this.readyResults, this.studentCache, 'student', 'fullStudentInfo', this.$student_backend)
        this.fetchDetails(this.readyResults, this.assignmentCache, 'assignment', 'fullAssignmentInfo', this.$assignment_backend)

        this.sortedResults = this.sortResults()  // TODO wait until details fetched since it affects sort order

        this.updateUnique()

      }, deep: true  // Watch nested objects for changes.
    }
  },

  methods: {
    onUpdatedInstructorComments (id, report) {
      this.$emit('onUpdatedInstructorComments', id, report)
    },

    fillFromCache(data, cache) {

      console.log('before filling from cache', this.readyResults )

      this.readyResults.forEach( res => {
        if (!res.fullStudentInfo) {
          // in cache?
          let cachedStudent = this.studentCache.find(s => s.id === res.student)
          if (cachedStudent && !cachedStudent.fetching) { res.fullStudentInfo = cachedStudent }
        }

        if (!res.fullAssignmentInfo) {
          // in cache?
          let cachedAssignment = this.assignmentCache.find(s => s.id === res.assignment)
          if (cachedAssignment && !cachedAssignment.fetching) { res.fullAssignmentInfo = cachedAssignment }
        }
      })

    },

    fetchDetails (dataArray, cache, type, fullInfoField, backend) {
      // Cache contains Student objects, or a placeholder { id: 4, fetching: true } if the data has been requested

      if (!this.readyResults) { console.log('no ready results...'); return }

      this.readyResults.forEach( res => {
        if (!res[fullInfoField]) {   // Has fill info?

          let resId = res[type]
          let cachedItem = cache.find( s => s.id === resId)
          if (cachedItem) {
            if (!cachedItem.fetching) { res.fullInfo = cachedItem }
          }

          else {
            let placeholder = { id: resId, fetching: true }
            cache.push(placeholder)

            backend.$fetchOne(resId).then(data => {
              res[fullInfoField] = data
              // console.log('have fetched has full info for', res)
              let cacheIndex = cache.findIndex(s => s.id === resId)
              if (cacheIndex != -1) {
                // either a fetching, or the full details
                if (cache[cacheIndex].fetching) {
                  cache[cacheIndex] = data
                }
              }
              else {
                cache.push(data)
              }

              this.fillFromCache(dataArray, cache)  // Update any other results for this student
              this.updateUnique()
          })
        }
      }
    })
  },

  sortResults() {

    // console.log('computing sorted results', )
    let sorted = []

    this.readyResults.forEach( r =>
      sorted.push(r)
    )

    // Sort by assignment and then by student
    sorted.sort( function(a, b) {

      // If the full info is not available, temporarily sort by assignment
      if (!a.fullStudentInfo || !a.fullAssignmentInfo || !b.fullStudentInfo || !b.fullAssignmentInfo) {
        return a.assignment - b.assignment
      }

      // If same assignment week, sort by student
      if (a.fullAssignmentInfo.week == b.fullAssignmentInfo.week) {
        return a.fullStudentInfo.name.toLowerCase().localeCompare(b.fullStudentInfo.name.toLowerCase())
      }
      // Otherwise, sort by assignment
      else {
        return a.fullAssignmentInfo.week - b.fullAssignmentInfo.week
      }
    })
    return sorted
  },

  updateUnique() {
    console.log('find unique names/asgnts ', this.results)

    let studentNames = this.sortedResults.map( res => {
      if (res.fullStudentInfo) { return res.fullStudentInfo.name }
      else { return `Student id ${res.student}` }
    })

    this.uniqueStudents = []
    studentNames.forEach( n => { if (!this.uniqueStudents.includes(n)) {this.uniqueStudents.push(n)}  })
    this.uniqueStudents.sort()


    let assignmentNames = this.sortedResults.map( res => {
      console.log(res)
      if (res.fullAssignmentInfo) { return `Week ${res.fullAssignmentInfo.week}` }
      else { return `Assignment id ${res.assignment}` }
    })

    console.log(assignmentNames)

    this.uniqueAssignments = []
    assignmentNames.forEach( n => { if (!this.uniqueAssignments.includes(n)) {this.uniqueAssignments.push(n)}  })
    this.uniqueAssignments.sort()
  }

}
}

</script>
