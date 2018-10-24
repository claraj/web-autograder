<!-- Results of one grading batch.  -->


<template>

  <div>
    <h3>Results</h3>
    <ul>
      <div v-if="readyResults.length">
        <li v-for="result in sortedResults">
          <GradeResultDetail
            v-bind:result="result"
            @onChildUpdatedInstructorComments="onChildUpdatedInstructorComments">
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
  // props, or properties - this component expects to get them from it's parent
  props: {
    readyResults: Array,
  },
  // while data is this components own internal state. It can send data to a child component, where it will become that child's prop.
  data() {
    return {
      sortedResults: [],
      studentCache: [],
      assignmentCache: []
    }
  },
  mounted() {
    console.log('RESULT list items:', this.readyResults)
  },
  watch: {
    readyResults: {
        handler: function(newVal, oldVal) {
          // fetch student info, fetch assignment info
          // what's the new result?
          console.log('ready results changed')
          this.fetchStudentAssignment()
          this.sortedResults = this.sort()
      }, deep: true
    }
  },

  methods: {
    onChildUpdatedInstructorComments(id, comments) {
    //  console.log('LIST must save comments for ', id, comments)
// todo emit to parent
      this.$emit('onChangedInstructorComments', id, comments)
    },

    fetchStudentAssignment() {

      console.log('fetch more data')
      this.readyResults.forEach( res => {
        // has student data?
        if (!res.fullStudentInfo) {

          // in cache?
          let cachedStudent = this.studentCache.filter( s => s.id === res.student)[0]
          if (cachedStudent) {
            res.fullStudentInfo = cachedStudent
          }
          else {
          this.$student_backend.$fetchOne(res.student).then(data =>{
            res.fullStudentInfo = data
            this.studentCache.push(data)
          })
        }
      }

      if (!res.fullAssignmentInfo) {


        let cachedAssignment = this.assignmentCache.filter( a => a.id === res.assignment )[0]
        if (cachedAssignment) { res.fullAssignmentInfo = cachedAssignment }
        else {

          this.$assignment_backend.$fetchOne(res.assignment).then(data => {
            res.fullAssignmentInfo = data
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

        //console.log('sortd res', sorted)

      // Sort by assignment and then by student
        sorted.sort( function(a, b) {
          if (!a.fullStudentInfo || !a.fullAssignmentInfo || !b.fullStudentInfo || !b.fullAssignmentInfo) {
            return a.assignment - b.assignment
          }
          if (a.fullAssignmentInfo.week == b.fullAssignmentInfo.week) {
            return a.fullStudentInfo.name.toLowerCase().localeCompare(b.fullStudentInfo.name.toLowerCase())
          }
          else {
            return a.fullAssignmentInfo.week.toLowerCase().localeCompare(b.fullAssignmentInfo.week.toLowerCase())
          }
      })
      return sorted
    }
  }
}

</script>
