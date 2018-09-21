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
  name: 'Grader Modules',
  components:  { ItemManager },
  data () {
    return {
      name: 'Grader Module',
      attributes: [
        { attr: 'id', display: 'id', noEdit: true, omitFromForms: true},
        { attr :'week', display: 'Week' },
        { attr: 'github_base', display: 'GitHub Base'},
      ],
      backend: this.$gradermodule_backend
    }
  },
  // computed: {
  //   backend: function () { return new Backend('gradermodule') },
//  },
}


</script>
