<template>

<div>
  <h2>Grader Results</h2>

  <p>Batch: {{ batch }}</p>
</div>

</template>


<script>


export default {
  name: 'GraderResults',
  // components: { SelectionList },   // ?
  data () {
    return {
      batch: String
    }
  },
  mounted() {
    // figure out most recent class and select selectedClass to that
    this.batch = this.$route.query.batch
    console.log('grade result param is ', this.$route.query)
  },
}

</script>
