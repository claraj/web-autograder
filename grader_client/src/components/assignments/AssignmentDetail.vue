<!-- details about one assignment, possibly students who have completed it?  -->

<template>

  <div v-if="assignment">
    <h2>Assignment {{assignment.week}}</h2>

    <p><span class="title">ID:</span> {{assignment.id}}</p>

    <p v-if="assignment.programming_class.name">
      <span class="title">Programming class:</span> {{assignment.programming_class.name}}, {{assignment.programming_class.semester_human_string}}
    </p>

    <p><span class="title">GitHub organization:</span> {{assignment.github_org}}</p>
    <p><span class="title">Week:</span> {{assignment.week}}</p>
    <p><span class="title">Github assignment base:</span> {{assignment.github_base}}</p>
    <p><span class="title">Instructor repo:</span> <a :href="assignment.instructor_repo">{{assignment.instructor_repo}}</a></p>
    <p><span class="title">D2L gradebook:</span> <a :href="assignment.d2l_gradebook_url">{{assignment.d2l_gradebook_url}}</a></p>
  </div>
  <div v-else>
    {{status}}
  </div>

</template>

<script>

export default {
  name: 'AssignmentDetail',
  data() {
    return {
      assignment: {},
      status: 'Loading assignment information...'
    }
  },
  mounted() {
    let assignment_id = this.$route.query.id
    this.$assignment_backend.$fetchOne(assignment_id).then(asgt => {
      this.assignment = asgt
      return this.$classes_backend.$fetchOne(asgt.programming_class)
    }).then(programming_class => {
      this.assignment.programming_class = programming_class
    }).catch(err => {
      console.log('error fetching assignment info', e)
      this.status = 'Error fetching assignment information'
    })
  }
}

</script>

<style>
</style>
