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

// import Backend from '@/backends/management_backend'

export default {
  name: 'Assignments',
  components:  { ItemManager },
  data () {
    return {
      name: 'Assignment',
      detailUrl: 'assignment',
      attributes: [
        { attr: 'id', display: 'id', noEdit: true, omitFromForms: true, linkToDetails: true},
        { attr :'week', display: 'Week', regex: /^.+$/, required:true, message: 'Name is required' },
        { attr: 'github_base', display: 'GitHub Base', regex: /^[a-zA-Z_\d-]+$/, required: true, message: 'GitHub base can only contain letters, numbers _ and -' },
        { attr: 'github_org', display: 'GitHub Organization', required:true },
        { attr: 'instructor_repo', display: 'Instructor Repo', required:true, hyperlink: true },
        { attr: 'd2l_gradebook_url', display: 'D2L Gradebook URL', hyperlink: true },
      ],
      backend: this.$assignment_backend

    }
  }
}


</script>
