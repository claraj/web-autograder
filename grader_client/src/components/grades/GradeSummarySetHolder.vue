<template>

  <div>
    <div v-if="grades.length > 0">
    <p v-for="grade in grades">
      <GradeResultSummary
        v-bind:result="grade"
        v-on:onUpdateInstructorComments="onUpdateInstructorComments">
      </GradeResultSummary>

      <button class="important-button" v-on:click="onRegrade(grade.id)">REGRADE {{grade.id}}</button>
    </p>
  </div>
    <div v-else>No grades</div>
  </div>

</template>


<script>

import GradeResultSummary from '@/components/grades/GradeResultSummary.vue'
export default {
    name: 'GradeSummarySetHolder',
    components: { GradeResultSummary },
    props: {
      grades: Array
    },
    methods: {
      onRegrade (id) {
        this.$emit('onRegrade', id)
      },
      onUpdateInstructorComments(id, data) {
        this.$emit('onUpdateInstructorComments', id, data)
      }
    }
}
</script>

<style>
  button {
    background-color:purple;
    color: white;
  }
</style>
