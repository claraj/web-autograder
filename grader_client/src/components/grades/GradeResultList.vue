<!-- Results of one grading batch.  -->
<template>
  <div>
    <ul>
      <div v-if="readyResults.length">
        <li v-for="result in sortedResults">
          <GradeResultDetail
            v-bind:result="result"
            @onUpdatedInstructorComments="onUpdatedInstructorComments">
          </GradeResultDetail>
        </li>
      </div>

      <div v-else>
        <p>No results</p>
      </div>
    </ul>
  </div>
</template>

<script>

import GradeResultDetail from './GradeResultDetail'

export default {
  name: "GradeResultsList",
  components: { GradeResultDetail },
  props: {
    readyResults: Array,
  },
  data() {
    return {
      sortedResults: [],
      studentCache: [],   // readyResults has the student's ID, this is for full student info objects
      assignmentCache: []  // as above, for assignments
    }
  },
  mounted() {
    // For any ready results, fetch the full student and assignment info.
    console.log('RESULT list items:', this.readyResults)
    this.fetchDetails()
    this.sortedResults = this.sort()  // Sort results
  },
  watch: {
    readyResults: {
      handler: function(newVal, oldVal) {
        // fetch student info, fetch assignment info
        // what's the new result?
        console.log('ready results changed')
        this.fetchDetails(this.readyResults, this.studentCache, 'student', 'fullStudentInfo', this.$student_backend)
        this.fetchDetails(this.readyResults, this.assignmentCache, 'assignment', 'fullAssignmentInfo', this.$assignment_backend)

        this.sortedResults = this.sort()  // TODO wait until details fetched since it affects sort order
      }, deep: true  // Watch nested objects for changes.
    }
  },

  methods: {
    onUpdatedInstructorComments (id, comments) {
      this.$emit('onUpdatedInstructorComments', id, comments)
    },

    fillFromCache(data, cache) {
      this.readyResults.forEach( res => {
        if (!res.fullStudentInfo) {
          // in cache?
          let cachedStudent = this.studentCache.find(s => s.id === res.student)
          if (cachedStudent && !cachedStudent.fetching) { res.fullStudentInfo = cachedStudent }
        }

        if (!res.fullAssignmentInfo) {
          // in cache?
          let cachedAssignment = this.assignmentCache.find(s => s.id === res.assigmment)
          if (cachedAssignment && !cachedAssignment.fetching) { res.fullAssignmentInfo = cachedAssignment }
        }
      })
    },

    fetchDetails (dataArray, cache, type, fullInfoField, backend) {
      // Cache contains Student objects, or a placeholder { id: 4, fetching: true } if the data has been requested
      console.log('fetch details starting data')

      this.readyResults.forEach( res => {
        if (!res[fullInfoField]) {   // Has fill info?

          let resId = res[type]

          let cachedItem = cache.find( s => s.id === resId)
          if (cachedItem) {
            console.log(`{type} info is cached or being fetched `)
            if (!cachedItem.fetching) { res.fullInfo = cachedItem }
          }

          else {
            let placeholder = { id: resId, fetching: true }
            cache.push(placeholder)

            backend.$fetchOne(resId).then(data => {
              res[fullInfoField] = data
              console.log('have fetched has full info for', res)

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
          })
        }
      }
    })
  },


  sort() {

    console.log('computing sorted results', )
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
  }
}
}

</script>
