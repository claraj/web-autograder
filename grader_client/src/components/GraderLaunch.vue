<template>

<div>
  <p>List of assignments and students for a particular semester

    dropdown box of semesters, most recent default

    - selectable list of students
    - selectable list of assignents

    - GO button


      </P>

    <select v-model="selectedClass" v-on:change="classChange">
      <option v-for="programmingClass in programmingClasses">{{semester}}</option>
    </select>

<div id="left">
    <!-- Assignments -->
    <SelectionList v-model="assignments"/>
</div>

<div>
    <!-- Students -->
    <SelectionList v-model="students"/>
</div>

  <button onClick="@startGrading">Start Grading</button>

</div>


</template>

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
    this.classChange()
  },
  methods: {

    getClasses() {
      this.$classes_backend.get().then( response => {
        this.programmingClasses = response
        if (this.programmingClasses) { this.selectedClass = this.programmingClasses[0] }
      })
    },

    classChange() {
      // Load this class's students, this class's assignments
      this.$student_backend.$query( { programmingclass: selectedClass })
      .then (response => {
        this.students = response
      })

      this.$assignment_backend.$query( {programmingClass: selectedClass})
        .then( response => {
          this.assignments = response
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
