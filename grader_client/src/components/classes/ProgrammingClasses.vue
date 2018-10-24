
<template>

  <ItemManager
    v-bind:name="name"
    v-bind:attributes="attributes"
    v-bind:backend="backend"
    v-bind:bulkCSVOrder="bulkCSVOrder"
  />
</template>

<script>

import ItemManager from '@/components/parts/ItemManager.vue'

// import Backend from '@/backends/management_backend'

export default {
  name: 'ProgrammingClasses',
  components:  { ItemManager },
  data () {
    return {
      name: 'Class',
      attributes: [
        { attr: 'id', display: 'ID', noEdit: true, omitFromForms: true },
        { attr: 'name', display: 'Name' },
        { attr: 'semester_code', display: 'Semester' },
        { attr: 'semester_human_string', display: 'Semester Name', noEdit: true },
      ],
      backend: this.$classes_backend
    }
  }
}


</script>
