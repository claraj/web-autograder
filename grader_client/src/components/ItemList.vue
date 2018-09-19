<template>

  <div>

    <p>HELLO THIS IS LIST</p>

    <table id="item-detail-table">

      <tr>
        <th v-for="attr in attributes">
        {{ attr.display }}</th>
      <th>Edit</th>
      <th>Delete</th>
    </tr>

      <tr v-for="item in items" v-bind:key="item.id">

        <td v-for="attr in attributes">{{ item[attr.attr] }}</td>
        <td><button @click="requestEdit(item.id)">Edit</button></td>
        <td><button @click="requestDelete(item.id)">Delete</button></td>
      </tr>

    </table>
  </div>
</template>


<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  tr,td,th,table {
    border: 1px solid black;
  }
</style>

<script>

/* eslint-disable */


export default {
  name: 'ItemList',
  props: {
    items: Array,
    attributes: Array,
    item: Object
  },

  mounted () {
    // this.fetchItems()
    console.log('item list mounted', this.items)
    console.log('student attrs', this.attributes)
  },

  methods: {
    requestEdit(itemId) {
      // this.item = this.items.filter( item => item.id === itemId)[0]
      console.log('emit edit message to parent for id', itemId)
      this.$emit('onRequestEdit', itemId)
    },
    requestDelete(itemId) {
      console.log('emit delete message to parent for id ', itemId)
    }

  }
}

</script>
