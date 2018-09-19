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

    <div v-for="attr in attributes">
      <label v-bind:for="attr.attr">{{ attr.display }}</label>
      <input v-bind:id="attr.attr" v-model="localItem[attr.attr]"/>
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
      console.log('edit local item changed ', this.item,  this.localItem)
    }
  }
,

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
        console.log(typeof data)
        if (data) { data = data.toString().trim() }
        this.localItem[attr.attr] = data


        // console.log('regex=', regex)
        // console.log('data=', data)
        // console.log('attr', attr)
        //
        // if (regex) {console.log('there\'s a regex')} else { console.log('noregex')}
        // if (regex && regex.test(data)) {console.log('regex matches')} else { console.log('no regex match validation fails')}

        if (regex && !regex.test(data) ) {
            this.errors.push(attr.message)
        }
      })

      console.log(this.errors)

      if (!this.errors.length) {
        console.log('no errors')
        this.$emit('onConfirmEdit', this.localItem)
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
    top: 70;
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
