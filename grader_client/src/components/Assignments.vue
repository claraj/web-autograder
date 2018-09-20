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
  name: 'Assignments',
  components:  { ItemManager },
  data () {
    return {
      name: 'Assignment',
      attributes: [
        { attr: 'id', display: 'id', noEdit: true, omitFromForms: true},
        { attr :'week', display: 'Week', regex: /^.+$/, required:true, message: 'Name is required' },
        { attr: 'github_base', display: 'GitHub Base', regex: /^[a-zA-Z_\d-]+$/, required: true, message: 'GitHub base can only contain letters, numbers _ and -' },
        { attr: 'instructor_repo', display: 'Instructor Repo', required:true },
        { attr:'d2l_gradebook_url', display: 'D2L Gradebook URL' },
        { attr: 'programming_class', display: 'Class Session'}
      ],
    bulkCSVOrder: "Week,GitHub_Base,Instructor_Repo,D2L_Url",
    }
  },
  computed: {
    backend: function () { return new Backend('assignment') }
  },
}


</script>
