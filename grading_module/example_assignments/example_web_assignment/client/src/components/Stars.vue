<template>
  <div v-bind:id="'star-'+_id">
    <!-- <input class="star-range-slider" v-model="starsSet" v-on:input="onStarsChanged" type="range" min="1" max="5"/> -->
    <input class="star-range-slider" v-model="starsSet" type="range" v-on:input="onStarsChanged" min="1" max="5"/>
    <span class="star-text-display">
      <span class="star-value">{{starsSet}}</span>
      <span v-if="starsSet==1">star</span>
      <span v-else>stars</span>
    </span>
  </div>
</template>

<script>

export default {
  name: 'Stars',
  props: {
    stars: Number, // initial number of stars, set by parent
    _id: String // _id of thing that has this number of stars
  },
  data () {
    return {
      starsSet: this.stars // This component's local copy, used to set value of range slider.
    }
  },
  watch: {
    stars: function () {
      console.log('hey stars changed')
      this.starsSet = this.stars
    }
  },
  methods: {
    onStarsChanged () {
      this.$emit('onStarsChanged', this._id, Number(this.starsSet))
    }
  }
}

</script>

<style scoped>
div {
  margin: 10px;
}
</style>
