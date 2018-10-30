<!-- For adding students and assignments to classes -->

<template>

  <div>
    <p>See links above for adding classes, students and assignments</p>

    <p>Select a class:</p>

    <select v-on:change="changeClass" v-model="classSelected">
      <option disabled value="">Select a class</option>
      <option v-for="programmingClass in programmingClasses" v-bind:value="programmingClass">
        {{programmingClass.name}} {{programmingClass.humanCode}}
      </option>
    </select>

    <h3>Current Assignments</h3>
    <ul><li v-for="assignment in assignmentsInClass">{{assignment}} Week {{assignment.week}} <a :href="assignment.instructor_repo">{{assignment.instructor_repo}}</a></li></ul>
    <h3>Current Students</h3>
    <ul><li v-for="student in studentsInClass">{{student.name}} {{student.github_id}}  {{student.star_id}}</li></ul>


    <h3>All Students</h3>

    <input v-model="studentFilter"/>

    <!-- <p v-if="!filteredStudents">No matches<p> -->
    <!-- <p v-else> -->
    <ul>
      <li v-for="student in filteredStudents">{{student.name}} {{student.github_id}}  {{student.star_id}}
      </li>
    </ul>
    <!-- </p>  -->

    <input v-model="assignmentFilter"/>

    <!-- <p v-if="!filteredAssignments">No matches<p> -->
    <ul><li v-for="assignment in filteredAssignments">Week {{assignment.week}} {{assignment.instructor_repo}}</li></ul>


  </div>

</template>
<script>

export default {
  name: 'Enrollment',
  data() {
    return {
      programmingClasses: [],
      classSelected: {},
      assignmentsInClass: [],
      studentsInClass: [],
      allStudents: [],
      allAssignments: [],
      studentFilter: '',
      assignmentFilter: ''
    }
  },
  computed: {
    filteredStudents: function() {
      console.log(this.studentFilter)
      if (!this.studentFilter) return this.allStudents
      return this.allStudents.filter( st => { return st.name.toLowerCase().includes(this.studentFilter.toLowerCase()) || st.github_id.includes(this.studentFilter)})
      // return this.allStudents.filter( st => { return st.name.toLowerCase().includes(this.studentFilter.toLowerCase()) })

    },
    filteredAssignments: function() {
      if (!this.assignmentFilter) return this.allAssignments
      return this.allAssignments.filter( as => { return as.week.toString().includes(this.assignmentFilter) || as.instructor_repo.toLowerCase().includes(this.assignmentFilter)})
    }
  },
  mounted() {
    this.getClasses()
  },
  methods: {
    getClasses() {
      this.$classes_backend.$fetchItems().then(data => { this.programmingClasses = data })
      this.$assignment_backend.$fetchItems().then(data => { this.allAssignments = data})
      this.$student_backend.$fetchItems().then(data => { this.allStudents = data })
    },
    changeClass() {
      //Load assignments, students for this class
      this.loadItemsForClass()
    },
    loadItemsForClass() {
      console.log('selection', this.classSelected)

      if (!this.classSelected) return

      this.$classes_backend.$itemsInCollection(this.classSelected.id, 'students').then(data => {
        this.studentsInClass = data
      })

      this.$classes_backend.$itemsInCollection(this.classSelected.id, 'assignments').then(data => {
        this.assignmentsInClass = data
      })
    }
  }
}


</script>
