<!-- All of the results for one grading batch. -->

<template>

<div>
  <h2>Grader Results</h2>

<div>
<P>TODO show list of assignments and names for this batch</p>

</div>


  <span>Batch {{ id }}</span>
  <span>Started at {{ batch.date | moment('ddd MMMM YYYY, HH:ss a')}}</span>
  <P><span>Expect {{expectedResults}} results,</span>
  <span>Received {{receivedResults}} results</span>
</p>
  <h3>Results</h3>

  <button v-if="loading" v-on:click="cancelPolling">Cancel</button>

  <p v-if="loading">Loading...</p>

<!-- TODO sort by assignment WEEK and then by student NAME -->
<!-- Links to student github page. -->

  <GradeResultList
    v-bind:readyResults="Object.values(this.gradedResults).filter(r => r!=null)"
    @onUpdatedInstructorComments="onUpdatedInstructorComments">
  </GradeResultList>


  <ul><li v-for="result in gradedResults">{{ result }} </li></ul>

  <p>{{gradedResults}}</p>

  <p v-if="loading">Loading...</p>

</div>

</template>


<script>

import GradeResultList from './GradeResultList'

const pollInterval = 3000
let poller

export default {
  name: 'GradeResult',
  components: { GradeResultList },
  data () {
    return {
      id: "",   // the batch id, passed in with a param from router
      batch: {},   // query server to get full batch info
      gradedResults: {},       // { 1: results1, 2: results2 ....}
      expectedResults: 0,
      receivedResults: 0,   // Received by the client, not processed on the back end
      loading: true
    }
  },

  computed: {
    readyResults: function() {
      // TODO why doesn't this work? Works with JS in component prop.
      console.log('computing ready results', this.gradedResults)
      let ready = Object.values(this.gradedResults).filter(r => r!=null)
      console.log('computed ready:', ready)
      return ready
    }
  },
  mounted() {

    console.log('The route query', this.$route.query)

    this.id = this.$route.query.id

    this.$gradertask_backend.$fetchOne(this.id).then( data => {
      console.log('batch info', data)
      this.batch = data
      this.expectedResults = this.batch.things_to_grade

      if (this.expectedResults == this.batch.processed) {
        console.log('this batch is complete, no polling')
        this.getLatestResults()   // this batch is completed
      }

      else {
        this.getLatestResults()
        poller = setInterval( this.getLatestResults, pollInterval);  // keep polling at intervals
        // TODO stop at some point
      }
    })
  },

  beforeRouteLeave(to, from, next) {
    console.log('leaving page and cancelling interval')
    clearInterval(poller)
    next()   /// todo this does not always work
  },

  methods: {

     onUpdatedInstructorComments(resultId, newComments) {
       console.log('will now update comments', resultId, newComments)
       this.$grade_backend.$editItem({id: resultId, instructor_comments: newComments } )
        .then( d => console.log(d))
        .catch(err => console.log(err))
     },

     cancelPolling() {
       this.loading = false
       clearInterval(poller)
     },

    getLatestResults() {

    //  console.log('polling grader, have this many results ', this.receivedResults)

      console.log('GET LATEST before polling')
      console.log(this.gradedResults)

      // If the server is reporting that everything is graded, stop future polls
      if (this.batch.processed >= this.batch.things_to_grade) {
        this.cancelPolling()
        console.log('clearing interval, server knows all the results')

      }

      this.$autograder_backend.$graderProgress(this.batch.id)
          .then( data => {
            // data should be a list of ids that have been graded
            console.log('polled and got this result', data)

            data.graded_ids.forEach( id => {
              console.log('process', id)
              if ( !this.gradedResults[String(id)] ) {
                //add this ID and set value to null
                this.gradedResults[String(id)] = null
              }

            })
          }).then( () => {

            console.log('now to get any missing data from this.gradedResults')

            console.log('graded valies', Object.values(this.gradedResults))
            console.log('graded values are null?', Object.values(this.gradedResults).find(r => r!=null))

            // if all done, stop.
            if (Object.values(this.gradedResults).find( r => r != null)) {
              console.log('there are no missing results.')
              this.cancelPolling()
            }


            for (let id in this.gradedResults) {

             console.log('get data for id', id, this.gradedResults[id])
              if (this.gradedResults[String(id)] == null)  {
                console.log('result ready, get details', id)


                this.$grade_backend.$fetchOne(String(id))
                  .then( data => {
                    this.receivedResults++ ;
                    console.log('data for one grade', data)
                    this.gradedResults[String(id)] = data
                    console.log('now graded results are', this.gradedResults)
                  })
              }
            }

          }).catch( err => {
            console.log('error, cancelling poller', err);
            this.cancelPolling() })


    },



  }
}

</script>
