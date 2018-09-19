<template>

  <div id="edit-modal" v-if="visible">
  <div id="edit-modal-content">

    <p>HELLO THIS IS MODAL</p>

    <h2>{{action}}</h2>
    <p v-if="errors.length"><b>Fix these errors: </b>
      <ul>
        <li v-for="error in errors">{{ error }}</li>
      </ul>
    </p>

    <label for="name">Name</label>
    <input id="name" required="true" v-model="name" />
    <br>
    <label for="github-id">GitHub ID</label>
    <input id="github-id" v-model="github_id"/>
    <br>
    <label for="org-id">Org ID</label>
    <input id="org-id" v-model="org_id" type="number"/>
    <br>
    <label for="star-id">Star ID</label>
    <input id="star-id" v-model="star_id"/>
    <br>
    <button @click="hideModal">Cancel</button>
    <button @click="checkForm">Save</button>
  </div>
  
</div>

</template>


<script>

/* eslint-disable */

export default {
  name: "AddEditItem",
  props: {
      item: Object,
      attributes: [],
      errors: [],
      visible: true,
      action: ""
  },
  methods: {
    hideModal () {
      console.log('hidemodal')
    },
    checkForm() {
      console.log('checkform')
    }
  }
}

</script>


<style>

  /* #edit-modal {
    position: fixed;
    z-index: 1;
    height: 100%;
    width: 100%;

    top: 0;
    right: 0;
  }

  #edit-modal-content {
    margin: 40% auto;
    padding: 40;
    background-color: lightgreen;
  }

  #edit-modal-content label {
    display: inline-block;
    vertical-align: middle;
    text-align: right;
    width: 100px;
  }

  #edit-modal-content input {
    display: inline-block;
    vertical-align: middle;
  }  */


</style>
