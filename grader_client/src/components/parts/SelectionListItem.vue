
<template>
<input v-model="item.selected" type="checkbox" v-on:click="itemSelected(item.id, item.selected)"/>
<span>{{prefix}} {{item.displayText}}</span>

</template>
