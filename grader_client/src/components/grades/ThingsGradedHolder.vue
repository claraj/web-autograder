<template>
  <div>
    <ThingsGradedList
      v-bind:students="students"
      v-bind:assignments="assignments"
      v-bind:programmingClass="programmingClass">
    </ThingsGradedList>
  </div>

</template>

<script>

import ThingsGradedList from '@/components/grades/ThingsGradedList'
export default {
  name: 'ThingsGradedHolder',
  components: { ThingsGradedList },
  props: {
    batch: Object
  },
  data() {
    return {
      students: [],
      assignments: [],
      programmingClass: {}
    }
  },
  mounted() {
    this.$classes_backend.$fetchOne(this.batch.programmingClass)
      .then(data => this.programmingClass = data )

    this.$util_backend.$studentsInBatch(this.batch.id)
      .then(data => {
          let names = data.map(s => s.name)
          this.students = names
        })

    this.$util_backend.$assignmentsInBatch(this.batch.id)
      .then(data => {
        let weeks = data.map(a => a.week )
        this.assignments = weeks
      })
  }
}

</script>

<style>

.title {
  font-weight: bold;
}

.div {
  text-align: left;
}
</style>
