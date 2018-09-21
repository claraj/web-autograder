<template>


<!--  List of things that are checkable -->
<div>
 <ul>
  <li v-for="item in items">
    <input v-model="item.selected" type="checkbox" onclick="@itemSelected(item.id)"/>
    <span>{{item.displayText}}</span>
  </li>
</ul>
</div>

</template>

<script>

export default {
  name: "SelectionList",
  props: {
    items: Array,
  },
  data() {
    return {

    }
  },
  methods: {
    itemSelected() {
      // emit to parent, id + selected (?)
      // or parent can watch?

    }
  }
}

</script>
