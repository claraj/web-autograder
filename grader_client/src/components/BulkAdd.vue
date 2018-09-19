<template>
<!--  for dumping a CSV and letting server figure it out -->


<div id="bulk-add">

  <p>HELLO THIS IS BULK ADD</p>


  <h2>Bulk Add</h2>
  <p>Provide data in CSV format in the order {{ instructions }}</p>
  <P>Missing fields are ok.</p>
  <textarea rows="6" columns="100" v-model="rawData"></textarea>
  <br>
  <button @click="bulkAdd">Upload</button>

  <ul>
    <li v-for="error in errors">{{ error }}</li>
  </ul>

  <p>{{ countAdded }} {{ countAdded | pluralize itemType }} added.</p>
</div>

</template>


<script>

/* eslint-disable */

export default {
  name: 'BulkAdd',
  data () {
    return {
      instructions: "put key list here in parent",
      itemType: "",
      rawData: "",
      countAdded: 0,
      errors: []
    }
  }
}
</script>


<style>
</style>
