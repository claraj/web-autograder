<template>
  <ItemManager
    v-bind:name="name"
    v-bind:attributes="attributes"
    v-bind:backend="backend"
  />
</template>

<script>

import ItemManager from './ItemManager.vue'

// import Backend from '@/backends/management_backend'

export default {
  name: 'Students',
  components:  { ItemManager },
  data () {
    return {
      name: 'Student',
      attributes: [
        { attr: 'id', display: 'id', noEdit: true, omitFromForms: true},
        { attr :'name', display: 'Name', regex: /^.+$/, required:true, message: 'Name is required' },
        { attr: 'github_id', display: 'Github ID', regex: /^[a-zA-Z_\d-]+$/, message: 'GitHub username can only contain letters, numbers _ and -' },
        { attr: 'org_id', display: 'MCTC ID', regex: /^\d{8}$/, message: 'MCTC id should be 8 numbers' },
        { attr: 'star_id', display:'Star ID', regex: /^[a-z]{2}\d{4}[a-z]{2}$/, message: 'Star ID must be in the form ab1234cd' },
        { attr: 'active', display: 'Active?', boolean: true, },
        { attr: 'programming_class', display: 'Class Session', dropdown: true, dropdownSource: this.$classes_backend }

      ],
      backend: this.$student_backend,
      // dropdownBackend: this.$classes_backend
    }
  }
}


</script>
