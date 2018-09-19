<template>

  <!--  for dumping a CSV and letting server figure it out -->

  <div id="bulk-add">

    <h2>Bulk Add {{itemType}}</h2>
    
    <p>Provide data in CSV format in the order
      <em>{{ instructions }}</em></p>
      <P>Missing fields are ok.</p>
        <textarea rows="6" columns="100" v-model="rawData"></textarea>
        <br>
        <button @click="bulkAdd">Upload</button>

        <ul>
          <li v-for="error in errors">{{ error }}</li>
        </ul>

        <p>{{countAdded}} {{ itemType }}(s) added.</p>
      </div>

    </template>


<script>

/* eslint-disable */

export default {
  name: 'BulkAdd',
  props: {
    instructions: String,
    itemType: String,
    countAdded: 0,
    errors: Array
  },
  data () {
    return {
      rawData: ""
    }
  },

  methods: {
    bulkAdd() {
      const text = this.rawData.trim()
      if (text) {
        this.$emit('onSubmitBulk', text)
      }
    }
  }
}

</script>


<style>

  textarea {
    width: 95%;
  }

</style>
