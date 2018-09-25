<template>

<div>
  <h2>Grader Results</h2>

  <p>Batch: {{ batch }}</p>
  <p>Expect {{expectedResults}} results</p>
  <p>Received {{receivedResults}} results</p>

  <h3>Results</h3>

  <button v-on:click="cancelPolling">Cancel</button>

  <p v-if="loading">Loading...</p>

<!-- TODO sort by assignment and then by student -->
<!-- Links to student github page. -->

  <ul><li v-for="thing in gradedResults">{{ thing }} </li></ul>

  <p>{{gradedResults}}</p>

  <p v-if="loading">Loading...</p>




</div>

</template>


<script>

const pollInterval = 3000
let poller

export default {
  name: 'GraderResults',
  // components: { SelectionList },   // ?
  data () {
    return {
      batch: "",
    //  gradedResultsIds = [],    // {1, 2, 3 ... }
      gradedResults: {},       // { 1: reults1, 2: results2 ....}
      expectedResults: 0,
      receivedResults: 0,
      loading: true
    }
  },
  mounted() {
    // figure out most recent class and select selectedClass to that
    this.batch = this.$route.query.batch
    this.expectedResults = this.$route.query.expected_results
    console.log('grade result param is ', this.$route.query)

    poller = setInterval( this.pollGrader, pollInterval);

  },

  beforeRouteLeave(to, from, next) {
    console.log('leaving page and cancelling interval')
    clearInterval(poller)
    next()   /// todo this does not always work

  },
   methods: {

     cancelPolling() {
       clearInterval(poller)

     },

    pollGrader() {

      console.log('polling grader, have this many results ', this.receivedResults)


      if (this.receivedResults >= this.expectedResults) {
        clearInterval(poller)
        this.loading = false
      }

        this.$autograder_backend.$pollGrader(this.batch)
          .then( data => {
            // data should be a list of ids that have been graded
            console.log('polled and got this result', data)

            data.graded_ids.forEach( id => {
              console.log('process', id)
              if ( !this.gradedResults[String(id)] ) {
                //add and set to null
                this.gradedResults[String(id)] = null
              }

              console.log('set gradedResults to', this.gradedResults)

            })
          }).then( () => {


            console.log('now to get any missing data from this.gradedResults')

            for (let id in this.gradedResults) {

              console.log('get data for id', id, this.gradedResults[id])
              if (this.gradedResults[String(id)] == null)  {
                console.log('result ready, get details', id)
                this.receivedResults++ ;
                this.$grade_backend.$fetchOne(String(id))
                  .then( data => {
                    console.log('data for one grade', data)
                    this.gradedResults[String(id)] = data
                  })
              }
            }

          }).catch( err => {
            console.log('error, cancelling poller', err);
            clearInterval(poller) })


    }

  }
}

</script>
