<!-- All of the results for one grading batch. -->

<template>

<div>
  <h2>Grader Results</h2>

  <p>Batch: {{ id }}</p>
  <P>Started at: GO GET DATE {{ batch.data}}</p>
  <p>Expect {{expectedResults}} results</p>
  <p>Received {{receivedResults}} results</p>

  <h3>Results</h3>

  <button v-on:click="cancelPolling">Cancel</button>

  <p v-if="loading">Loading...</p>

<!-- TODO sort by assignment WEEK and then by student NAME -->
<!-- Links to student github page. -->

  <GradeResultList
    v-bind:readyResults="Object.values(this.gradedResults).filter(r => r!=null)"
    @onChangedInstructorComments="onChangedInstructorComments">
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
      id: "",
      batch: {},
    //  gradedResultsIds = [],    // {1, 2, 3 ... }
      gradedResults: {},       // { 1: results1, 2: results2 ....}
      expectedResults: 0,
      receivedResults: 0,
      loading: true
    }
  },

  computed: {
    readyResults: function() {

      // is param?

      // TODO why doesn't this work? Works with JS in component prop.
      console.log(this.gradedResults)
      let ready = Object.values(this.gradedResults).filter(r => r!=null)
      console.log('computed ready:', ready)
      return ready
    }
  },
  mounted() {

    // Is this a completed batch?

    // Or is it newly launched and waiting on results?

    // figure out most recent class and select selectedClass to that

    console.log(this.$route.query)

    this.batch = this.$route.query.id
    this.expectedResults = this.$route.query.expected_results
  //  console.log('grade result param is ', this.$route.query)

    // get grade batch info

    this.$gradertask_backend.$fetchOne(this.batch).then( data => {



    }).then()


    this.pollGrader()   // first poll
    poller = setInterval( this.pollGrader, pollInterval);  // keep polling at intervals

  },

  beforeRouteLeave(to, from, next) {
    console.log('leaving page and cancelling interval')
    clearInterval(poller)
    next()   /// todo this does not always work

  },
   methods: {

     onChangedInstructorComments(resultId, newComments) {
       console.log('will now update comments', resultId, newComments)
       this.$grade_backend.$editItem({id: resultId, instructor_comments: newComments } )
        .then( d=> console.log(d))
        .catch(err => console.log(err))
     },

     cancelPolling() {
       clearInterval(poller)

     },

    pollGrader() {

    //  console.log('polling grader, have this many results ', this.receivedResults)


      if (this.receivedResults >= this.expectedResults) {
        clearInterval(poller)
        this.loading = false
      }

        this.$autograder_backend.$pollGrader(this.batch)
          .then( data => {
            // data should be a list of ids that have been graded
        //    console.log('polled and got this result', data)

            data.graded_ids.forEach( id => {
        //      console.log('process', id)
              if ( !this.gradedResults[String(id)] ) {
                //add and set to null
                this.gradedResults[String(id)] = null
              }

        //      console.log('set gradedResults to', this.gradedResults)

            })
          }).then( () => {


      //      console.log('now to get any missing data from this.gradedResults')

            for (let id in this.gradedResults) {

        //      console.log('get data for id', id, this.gradedResults[id])
              if (this.gradedResults[String(id)] == null)  {
        //        console.log('result ready, get details', id)
                this.receivedResults++ ;
                this.$grade_backend.$fetchOne(String(id))
                  .then( data => {
                //    console.log('data for one grade', data)
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
