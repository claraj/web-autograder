<template>

  <div>

    <h2>{{ itemType }} List</h2>

    <table id="item-detail-table">

      <tr>
        <th v-for="attr in attributes">
        {{ attr.display }}</th>
      <th>Edit</th>
      <th>Delete</th>
    </tr>

      <tr v-for="item in items" v-bind:key="item.id">

        <td v-for="attr in attributes">
            <template v-if="attr.hyperlink"><a v-bind:href="item[attr.attr]">{{ item[attr.attr] }}</a> </template>
            <template v-else-if="attr.linkToDetails"><router-link :to="{ name: detailUrl, params: { id: item[attr.attr] }}">{{ item[attr.attr] }}</router-link></template>
            <template v-else-if="attr.boolean"><input type="checkbox" v-bind:checked="item[attr.attr]" disabled="true"/> </template>
            <template v-else> {{ item[attr.attr] }} </template>
        </td>

        <td><button class="neutral-button" @click="requestEdit(item.id)">Edit</button></td>
        <td><button class="danger-button" @click="requestDelete(item.id)">Delete</button></td>
      </tr>

    </table>
  </div>
</template>

<script>

export default {
  name: 'ItemList',
  props: {
    items: Array,
    attributes: Array,
    item: Object,
    itemType: String,
    detailUrl: String
  },
  mounted () {
  },
  methods: {
    requestEdit(itemId) {
      // this.item = this.items.filter( item => item.id === itemId)[0]
      console.log('emit edit message to parent for id', itemId)
      this.$emit('onRequestEdit', itemId)
    },
    requestDelete(itemId) {
      console.log('emit delete message to parent for id ', itemId)
      this.$emit('onRequestDelete', itemId)
    }
  }
}

</script>

<style>
  table {
    width: 100%;
    border-collapse: collapse;
  }
  tr,td,th,table {
    border: 1px solid black;
  }
</style>
