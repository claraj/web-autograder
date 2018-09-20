
<template>

  
  <ItemManager
    v-bind:name="name"
    v-bind:attributes="attributes"
    v-bind:backend="backend"
    v-bind:bulkCSVOrder="bulkCSVOrder"
  />
</template>

<script>

import ItemManager from './ItemManager.vue'

import Backend from '@/backends/management_backend'

export default {
  name: 'Classes',
  components:  { ItemManager },
  data () {
    return {
      name: 'Class',
      attributes: [
        { attr: 'id', display: 'ID' },
        { attr: 'name', display: 'Name' },
        { attr: 'semester_code', display: 'Semester' },
      ],
    }
  },
  computed: {
    backend: function () { return new Backend('class') },
  },
}


</script>
