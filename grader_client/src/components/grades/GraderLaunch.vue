<!-- Dropdown of classes, ability to select assignments, students for that class, and start grading process. -->
<template>

<div>
  <h2>Grader Launch</h2>

  <h3>Programming Classes <router-link to="classes"><img src="@/assets/intersect_color.png"></router-link></h3>

  <select v-model="selectedClass" v-on:change="classSelectionChanged">
    <option v-for="programmingClass in programmingClasses" v-bind:value="programmingClass.id" v-bind:key="programmingClass.id">ID {{programmingClass.id}}: {{programmingClass.name}}, {{programmingClass.semester_code}}</option>
  </select>

  <p>Select students and assignments to grade<p>

    <button v-on:click="startGrading">Start Grading</button>
    <p class="error">{{error}}</p>

    <div class="grid-container">
      <div class="row">
        <h3>Assigments <router-link to="assignments"><img src="@/assets/intersect_color.png"></router-link>
        </h3>
        <SelectionList v-bind:items="assignments" v-bind:prefix="assignmentPrefix"/>
      </div>

      <div class="row">
        <h3>Students <router-link to="students"><img src="@/assets/intersect_color.png"></router-link></h3>
        <SelectionList  v-bind:items="students" v-bind:prefix="studentPrefix"/>

      </div>
    </div>
  </div>

</template>

<script>

import SelectionList from '@/components/parts/SelectionList'

export default {
  name: 'GraderLaunch',
  components: { SelectionList },
  data () {
    return {
      programmingClasses: [],
      students: [], // alll the students
      assignments: [], // alll the assignments
      selectedClass: '',
      error: '',
      studentPrefix: 'Name: ',
      assignmentPrefix: 'Week: '
    }
  },
  mounted () {
    // figure out most recent class and select selectedClass to that
    this.getClasses()
  },
  watch: {
    selectedClass: function () {
      this.classSelectionChanged() // no arrow functions because this is bound to the wrong thing
    }
  },
  methods: {
    getClasses () {
      this.$classes_backend.$fetchItems().then(response => {
        this.programmingClasses = response
        console.log('here is the response', response)
        if (this.programmingClasses) {
          console.log('setting selected class to', this.programmingClasses[0])
          this.selectedClass = this.programmingClasses[0].id
        }
      })
    },
    classSelectionChanged () {
      if (!this.selectedClass) { return }

      this.$util_backend.$fetchProgrammingClassStudents(this.selectedClass)
        .then(data => {
          this.students = data
          if (this.students) {
            this.students.forEach(student => { student.displayText = student.name })
          }
        })

      this.$util_backend.$fetchProgrammingClassAssignments(this.selectedClass)
        .then(data => {
          this.assignments = data
          if (this.assignments) {
            this.assignments.forEach(a => { a.displayText = a.week })
          }
        })
    },
    startGrading () {
      let selectedStudents = this.students.filter(student => student.selected).map(student => student.id)
      let selectedAssignments = this.assignments.filter(assignment => assignment.selected).map(assignment => assignment.id)

      if (!selectedStudents.length || !selectedAssignments.length) {
        this.error = 'Select at least one student and at least one assignment'
        return
      }
      console.log(this.selectedClass)
      this.error = ''
      let data = {students: selectedStudents, assignments: selectedAssignments, programming_class: this.selectedClass}

      let expectedResults = selectedStudents.length * selectedAssignments.length

      console.log('grader will send', data)

      this.$autograder_backend.$invoke(data)
        .then(response => {
          console.log('response from server', response)
          this.$router.push({name: 'grader-results', query: {id: response.batch, expectedResults: expectedResults}})
        })
        .catch(err => {
          console.log('error launching ', err)
        })
    }
  }
}

</script>

<style>
  .grid-container {
    display: grid;
    grid-template-columns: auto auto;
  }

  .error {
    font-weight: bold;
    color: darkred;
  }
</style>
