<template>

  <div id="edit-modal" v-if="visible">
  <div id="edit-modal-content">

    <h2>{{action}}</h2>

    <p v-if="errors.length"><b>Fix these errors: </b>
      <ul>
        <li v-for="error in errors">{{ error }}</li>
      </ul>
    </p>

    <div v-for="attr in attributes">
      <div v-if="!attr.omitFromForms" >
        <label v-bind:for="attr.attr">{{ attr.display }}</label>
        <input v-bind:id="attr.attr" v-model="localItem[attr.attr]" :disabled="attr.noEdit" />
      </div>
    </div>

    <button @click="cancel">Cancel</button>
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
      attributes: Array,
      visible: Boolean,
      action: String
  },
  data () {
    return {
      localItem: Object.assign( {}, this.item),
      errors: [],
    }
  },

  watch: {
    item: function (newVal, oldVal) {
      this.localItem = Object.assign( {}, this.item)
  //    console.log('edit local item changed ', this.item,  this.localItem)
    }
  },

  methods: {

    cancel () {
      this.$emit('onCancel')
    },

    checkForm() {

      this.errors = []

      console.log('local item', this.localItem)
      console.log('attributes', this.attributes)

      this.attributes.forEach( attr =>  {

        const regex = attr['regex']
        let data = this.localItem[attr.attr]
        let required = attr['required']
        if (data) { data = data.toString().trim() }
        this.localItem[attr.attr] = data

        if (required && !data) {
          this.errors.push(attr.display + ' is required.')
        }

        // If there is data, and a regex, and the data fails the regex test
        if (data && regex && !regex.test(data) ) {
            this.errors.push(attr.message)
        }
      })

      console.log(this.errors)

      if (!this.errors.length) {
        console.log('no errors')
        this.$emit('onConfirmSubmit', this.localItem)
      } else {
        console.log('validation errors:', this.errors)
      }
    },

  }
}

</script>


<style>

  #edit-modal {
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
  }


</style>
