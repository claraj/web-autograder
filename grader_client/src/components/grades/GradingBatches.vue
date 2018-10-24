<!--  List of grading tasks that have been invoked.
Can view results in a GraderResults component, and delete old grading batches.   -->

<template>

<div>

  <h2>Grading Batches</h2>

  <!-- <SelectionList
    v-bind:items="batches"
  /> -->


  <p v-for="batch in batches">

    <router-link :to="{ name: 'grader-results', query: {id: batch.id} }">
      {{ batch.id }}
    </router-link>

    started at {{ batch.date | moment("dddd, MMMM Do YYYY hh:mm")}}.
  </p>

  <button v-on="delete_selected">delete selected</button>

</div>
</template>

<script>

import SelectionList from '@/components/parts/SelectionList.vue'

// import Backend from '@/backends/management_backend'

export default {
  name: 'GraderModules',
  components:  { SelectionList },
  data () {
    return {
      batches: [],
    }
  },

mounted() {
  // backend fetch all tasks TODO paginate?
  this.$gradertask_backend.$fetchItems().then( (data) => {
    console.log(data)
    this.batches = data
    this.batches.forEach(item => { item.selected = false })
  })
},
delete_selected() {
  //todo are you suuuuurrrre?
  let ids = batches.filter( item => item.selected ).map( item => item.id )
  this.$gradertask_backend.deleteMany(ids)
},

on_item_selected(id, isSelected) {
  console.log('prep for delete...')
  this.batches.forEach(item => { if (item.id === id) { item.selected = isSelected} })
}
}


</script>
