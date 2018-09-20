<template>

  <div id="class-management">
  </div>

</template>

<script>

import ItemList from './ItemList.vue'
import AddEditItem from './AddEditItem.vue'



export default {
    name = 'ClassManagement',
    components = { ItemList, AddEditItem },
    data () {
      return {
        classes: [],
        attributes: [
          { attr: 'id', display: 'ID' },
          { attr: 'name', display: 'Name' },
          { attr: 'semester_code', display: 'Semester' },
        ],
        focusClass: {},
        itemType: 'Classes',
        showAddEditModal: false,

      }
    },
    mounted () {
      this.fetchClasses();
    },
    methods: {
      this.$backend.fetchClasses().then( data => {
        this.classes = data;
      })

    }
}

</script>

<style>
</style>
