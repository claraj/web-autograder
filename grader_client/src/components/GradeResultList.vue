<template>

  <div>
    <h3>Results</h3>
    <ul>
      <div v-if="results.length">
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
  props: {
    results: Array
  },
  data() {
    return {
      sortedResults: []
    }
  },
  mounted() {
    console.log('list items:', this.results)
  },

  watch: {

    results: function() {

      this.sortedResults = []

      this.results.forEach( r =>
        this.sortedResults.push(r)
      )

    // Sort by assignment and then by student
      this.sortedResults.sort( (a, b) => {
      if (a.assignment.week == b.assignment.week) {
        return a.student.name < b.student.name
      }
      else {
        return a.assignment.week < b.assignment.week
      }
    })
  },
},

  methods: {
    onChildUpdatedInstructorComments(id, comments) {
      console.log('LIST must save comments for ', id, comments)
// todo emit to parent
      this.$emit('onChangedInstructorComments', id, comments)
    }
  }
}

</script>
