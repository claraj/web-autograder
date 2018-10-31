<template>
  <ItemManager
    v-bind:name="name"
    v-bind:detailUrl="detailUrl"
    v-bind:attributes="attributes"
    v-bind:backend="backend"
  />
</template>

<script>

import ItemManager from '@/components/parts/ItemManager.vue'

export default {
  name: 'Students',
  components:  { ItemManager },
  data () {
    return {
      name: 'Student',
      detailUrl: 'student',
      attributes: [
        { attr: 'id', display: 'id', noEdit: true, omitFromForms: true, linkToDetails: true},
        { attr :'name', display: 'Name', regex: /^.+$/, required:true, message: 'Name is required',  },
        { attr: 'github_id', display: 'Github ID', regex: /^[a-zA-Z_\d-]+$/, message: 'GitHub username can only contain letters, numbers _ and -' },
        { attr: 'org_id', display: 'MCTC ID', regex: /^\d{8}$/, message: 'MCTC id should be 8 numbers' },
        { attr: 'star_id', display:'Star ID', regex: /^[a-z]{2}\d{4}[a-z]{2}$/, message: 'Star ID must be in the form ab1234cd' },
        { attr: 'active', display: 'Active?', boolean: true, },
      ],
      backend: this.$student_backend,
    }
  }
}
</script>
