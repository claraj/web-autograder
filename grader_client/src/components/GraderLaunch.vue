<template>

<div>

  <h2>Grader Launch</h2>

  <p>
      </P>

    <select v-model="selectedClass" v-on:change="classSelectionChanged">
      <option v-for="programmingClass in programmingClasses" v-bind:value="programmingClass.id">ID {{programmingClass.id}}: {{programmingClass.name}}, {{programmingClass.semester_code}}</option>
    </select>

      <br><router-link to="classes">Add or edit programming classes?</router-link>

<p>Select students and assignments to grade.<p>

  <button onClick="startGrading">Start Grading</button>


<div class="grid-container">
<div class="row">
    <!-- Assignments -->
    <h3>Assigments</h3>
    <router-link to="assignments">Add or edit assignments?</router-link>
    <SelectionList v-bind:items="assignments"/>
</div>

<div class="row">
  <h3>Student</h3>
  <!-- Students -->
    <router-link to="students">Add or Edit Students?</router-link>
    <SelectionList  v-bind:items="students"/>

</div>
</div>



</div>


</template>

<style>

.grid-container {
  display: grid;
  grid-template-columns: auto auto;
}



</style>

<script>

import SelectionList from './SelectionList'

export default {
  name: 'GraderLaunch',
  components: { SelectionList },
  data () {
    return {
      programmingClasses: [],
      selectedClass: {},
      students: [],
      assignments: [],
      selectedClass: "",
    }
  },
  mounted() {
    // figure out most recent class and select selectedClass to that
    this.getClasses()
  },
  watch: {
    selectedClass: function() {this.classSelectionChanged() }  // no arrow functions because this is bound to the wrong thing
  },
  methods: {

    getClasses() {
      this.$classes_backend.$fetchItems().then( response => {
        this.programmingClasses = response
        console.log('here is the response', response)
        if (this.programmingClasses) {
          console.log('setting selected class to', this.programmingClasses[0])
          this.selectedClass = this.programmingClasses[0].id
        }
  //      this.classSelectionChanged()  // since changing selectedClass change the class seletion, the event is fired for us
      })

    },

    classSelectionChanged() {

      console.log('selection changed, selected class', this.selectedClass)
      if (!this.selectedClass) { return; }

      console.log('seec class if', this.selectedClass.id)

      this.$student_backend.$query( { programming_class: this.selectedClass } )
        .then( response => {
          console.log('student response', response)
          this.students = response.data
          console.log('students', this.students)
          if (this.students) {
            this.students.forEach( student => { student.displayText = student.name })
          }
      })

      this.$assignment_backend.$query( { programming_class: this.selectedClass })
        .then( response => {
          console.log('Assigments=', response)
          this.assignments = response.data
          if (this.assignments) {
            this.assignments.forEach( a => { a.displayText = a.week })
          }
      })
    },

    startGrading() {
      let selectedStudents = this.students.filter( student => student.selected ).map( student => student.id )
      let selectedAssignments = this.assignments.filter( assignment => assignment.selected).map(assignment => assignment.id)

      this.$grader_backend.invokeGrader( {students: selectedStudents, assignments: selectedAssignments}).then(response => {
        this.$router.push('GraderResults')
      })

    },

  }
}

</script>
