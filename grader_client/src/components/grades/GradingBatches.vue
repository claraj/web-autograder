<!--  List of grading tasks that have been invoked.
Can view results in a GraderResults component, and delete old grading batches.   -->

<template>

  <div>

    <h2>Grading Batches</h2>

    <!-- <SelectionList
    v-bind:items="batches"
    /> -->

    <div v-if="batches">
      <span>All</span>
      <input type="checkbox" v-model="selectAll" v-on:click="all()">
    </div>

    <p v-for="batch in batches">

      <input type="checkbox" v-model="batch.selected">
      <router-link :to="{ name: 'grader-results', query: {id: batch.id} }">
        {{ batch.id }}
      </router-link>

      started at {{ batch.date | moment("dddd, MMMM Do YYYY hh:mm")}}.
    </p>

    <button v-on:click="delete_selected">delete selected</button>

  </div>
</template>

<script>

import SelectionList from '@/components/parts/SelectionList.vue'

export default {
  name: 'GraderModules',
  components:  { SelectionList },
  data () {
    return {
      batches: [],
      selectAll: false
    }
  },
  mounted() {
    // backend fetch all tasks TODO paginate?
    this.getBatches()
  },
  methods: {
    getBatches() {
      this.$gradertask_backend.$fetchItems().then( (data) => {
        console.log(data)
        this.batches = data
        this.batches.forEach(item => { item.selected = false })
      })
    },
    delete_selected() {
      if (confirm('Are you sure you want to delete these batches?')) {
        let ids = this.batches.filter( item => item.selected ).map( item => item.id )
        this.$gradertask_backend.$deleteMany({ids}).then( () => {
          this.getBatches()
        })
      }
    },
    all() {
      this.batches.forEach(item => item.selected = !this.selectAll)
    },
    on_item_selected(id, isSelected) {
      console.log('prep for delete...')
      this.batches.forEach(item => { if (item.id === id) { item.selected = isSelected} })
    }
  }
}


</script>
