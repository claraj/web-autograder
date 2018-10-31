<!-- All of the results for one grading batch. -->

<template>

<div id="content">
<div>
  <h2>Grader Results for batch {{ id }}</span> <br>
    <span><span class="title">Started at</span> {{ batch.date | moment('ddd MMMM YYYY, HH:ss a')}}</span></h2>

<div>

</div>


  <P><span class="title">Stats: </span><span>Expect {{expectedResults}} results,</span>
  <span>Received {{receivedResults}} results</span>
</p>

  <button v-if="loading" v-on:click="cancelPolling">Cancel</button>

  <p v-if="loading">Loading...</p>
  <p class="error" v-if="timedOut">Timed out</p>

  <!-- <h3>Results</h3> -->

  <GradeResultList
    v-bind:readyResults="Object.values(this.gradedResults).filter(r => r!=null)"
    @onUpdateInstructorComments="onUpdateInstructorComments">
  </GradeResultList>


  <p v-if="loading">Loading...</p>

</div>
</div>

</template>


<script>

import GradeResultList from './GradeResultList'

const pollInterval = 3000
const timeout =  5 * 60 * 1000 // 5 minutes
const maxPollCount = timeout / pollInterval

// let this.poller

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
      loading: true,
      timedOut: false,
      pollCount: 0,
      poller: {}
    }
  },

  computed: {
    readyResults: function() {
      // TODO why doesn't this work? Works with JS in component prop.
      // console.log('computing ready results', this.gradedResults)
      let ready = Object.values(this.gradedResults).filter(r => r!=null)
      // console.log('computed ready:', ready)
      return ready
    }
  },
  mounted() {

    this.id = this.$route.query.id
    this.$gradertask_backend.$fetchOne(this.id).then( data => {
      this.batch = data
      this.expectedResults = this.batch.things_to_grade
      if (this.expectedResults == this.batch.processed) {
        this.getLatestResults()   // this batch is completed
      }

      else {
        this.getLatestResults()
        this.poller = setInterval( this.getLatestResults, pollInterval);  // keep polling at intervals
      }
    })
  },

  beforeRouteLeave(to, from, next) {
    console.log('leaving page and cancelling interval')
    this.cancelPolling()
    next()   /// todo this does not always work
  },
  beforeDestroy () {
    this.cancelPolling()
  },

  methods: {

     onUpdateInstructorComments(resultId, report) {
       console.log('will now update comments', resultId, report)
       this.$grade_backend.$editItem({id: resultId, generated_report: report } )
        .then( d => console.log(d))
        .catch(err => console.log(err))
     },

     cancelPolling() {
       this.loading = false
       clearInterval(this.poller)
     },

    getLatestResults() {

      this.pollCount++
      console.log('poll count', this.pollCount)

      if (this.pollCount > maxPollCount) {
        console.log('stop polling')
        this.timedOut = true
        this.cancelPolling()
      }

      if (this.batch.processed >= this.batch.things_to_grade) {
        this.cancelPolling()
      }

      this.$autograder_backend.$graderProgress(this.batch.id)
          .then( data => {
            // data should be a list of ids that have been graded

            data.graded_ids.forEach( id => {
              if ( !this.gradedResults[String(id)] ) {
                this.gradedResults[String(id)] = null  //add this ID and set value to null, will fetch full data later
              }

            })
          }).then( () => {

            // if all done, stop.
            if (Object.values(this.gradedResults).find( r => r != null)) {
              this.cancelPolling()
            }

            for (let id in this.gradedResults) {

              if (this.gradedResults[String(id)] == null)  {
                this.$grade_backend.$fetchOne(String(id))
                  .then( data => {
                    this.receivedResults++ ;
                    this.gradedResults[String(id)] = data
                  })
              }
            }

          }).catch( err => {
            console.log('error, cancelling this.poller', err);
            this.cancelPolling() })
    },

  }
}

</script>

<style>

.error {
  color: red;
}

#content {
  text-align: left;
}



</style>
