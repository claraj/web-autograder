

<template>

  <div>
    <h1>{{name}} Management</h1>

    <ItemList
      v-bind:items="items"
      v-bind:attributes="attributes"
      v-bind:itemType="itemType"
      @onRequestEdit="onRequestEdit"
      @onRequestDelete="onRequestDelete"
    />

    <div id="newItem">
      <h2>Add New {{name}}</h2>
      <button @click="showAddItemModal">Add new {{name}}</button>
    </div>

    <AddEditItem
      v-bind:visible="showAddEditModal"
      v-bind:item="focusItem"
      v-bind:attributes="attributes"
      v-bind:action="action"
      v-bind:errors="errors"
      v-bind:name="name"
      @onConfirmAddEditSubmit="onConfirmAddEditSubmit"
      @onCancelAddEdit="onCancelAddEdit"
    />

    <BulkAdd
      v-bind:instructions="bulkCSVOrder"
      v-bind:errors="bulkErrors"
      v-bind:countAdded="bulkItemsAdded"
      v-bind:itemType="itemType"
      @onSubmitBulk="onSubmitBulk"
      />

  </div>
</template>


<style>
  #newItem {
    padding: 15px;
  }
</style>


<script>

/* eslint-disable */

var pluralize = require('pluralize')

import ItemList from '../components/ItemList.vue'
import BulkAdd from '../components//BulkAdd.vue'
import AddEditItem from '../components/AddEditItem.vue'

export default {
  name: 'ItemManager',
  components: { ItemList, BulkAdd, AddEditItem },
  props: {

      // focusItem: Object,
      // showAddEditModal: Boolean,
      // action: "",
      // bulkErrors: [],
      // bulkItemsAdded: 0,
      attributes: Array,
      name: String,
      bulkCSVOrder: String,
      backend: Object,
      // errors: Array
  },
  data () {
  return {
    items: [],
    focusItem: {},
    showAddEditModal: false,
    action: "",
    bulkErrors: [],
    bulkItemsAdded: 0,
    // attributes: Array,
    // name: String,
    // bulkCSVOrder: String,
    // backend: Object,
    errors: []

  }},
  computed: {
    itemType: function () {
      return pluralize(this.name);
    }
  },

  mounted () {
    this.fetchItems()
  },

  methods: {

    /* Fetching items from server */
    fetchItems() {
      // console.log('item manager backend', this.backend)
      this.backend.$fetchItems().then(data => {
        this.items = data
        console.log('Item component fetched these items', this.items)
      })
    },

    onConfirmAddEditSubmit(item) {
      this.focusItem = item
      if (this.action.startsWith('Add')) {
        this.addItem()
      }
      else {
        this.editItem();
      }
    },

    /* Editing item info */
    onRequestEdit(id) {
      // populate the AddEditItem component with the selected item
      console.log('recived request to edit ', id)
      this.focusItem = this.items.filter( item => item.id === id)[0]
      console.log('to edit:', this.focusItem)
      if (this.focusItem) {
        // todo remove ID, should not be edited
        this.showAddEditModal = true
        this.action = 'Edit'
      }
    },

    // Backend request edit
    editItem() {
      const data = this.focusItem; // { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      this.backend.$editItem(data).then( () => {
          this.focusItem = {}
          this.showAddEditModal = false;
          this.fetchItems()
        })
    },

    onCancelAddEdit() {
      this.showAddEditModal = false;
    },

    /* Adding items */
    showAddItemModal() {
      this.focusItem = {}
      this.action = "Add"
      this.showAddEditModal = true;
    },

    addItem() {
      const data = this.focusItem; // { id: this.id, name: this.name, star_id: this.star_id, org_id: this.org_id, github_id:this.github_id }
      this.backend.$addItem(data).then( () => {
        this.focusItem = {}
        this.fetchItems()
      })
    },

    onSubmitBulk(rawData) {
      console.log('app bulk add')
      console.log(rawData)
      this.backend$bulkAddItem(rawData).then( (resp) => {
        console.log('server response', resp)
        // this.rawData = ""
        this.bulkItemsAdded = resp.created
        this.bulkErrors = resp.errors
        this.fetchItems();
      })
    },

    /* Deleting items */
    onRequestDelete(id) {
      console.log('delete item ', id)
      const item = this.items.filter(item => item.id === id)[0]
      if (item)
      if (confirm(`Delete item for week ${item.week}?`)){
        this.backend.$deleteItem(id).then( () => {
          this.fetchItems()
        })
      }
    }

  }
}

</script>
