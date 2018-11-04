<template>
  <div>


    <div id="text-report">
      <p><pre ref="fullReportText" id="full-report-text">{{text}}</pre></p>
      <input id="mirror-text-report" :value="text"></input>
      <button @click="hide">Close</button>
      <button @click.stop.prevent="copyText">Copy</button>
      <span v-show="copied">Copied to clipboard</span>
    </div>


  </div>
</template>

<script>

export default {
  name: 'GradeTextReport',
  data() {
    return {
        copied: false
    }
  },
  props: {
    text: String
  },
  methods: {
    copyText() {
        let textHolder = document.querySelector('#mirror-text-report')
        textHolder.select()
        document.execCommand('copy')
          this.copied = true
        let vue = this
        setTimeout( function() {vue.copied = false}, 2000)
    },
    hide() {
      this.$emit.hideTextReport()
    }
  }

}
</script>

<style>
  #text-report {
    position: absolute;
    width: 80%;
    height: 500px;
    z-index: 10;
    top: 50%;
    margin: auto;
    left: 50%;
    /* margin: -100px 0 0 -150px; */
    border: 1px darkgray solid;
    background-color: white;
    transform: translate(-50%, -50%);
    box-shadow: 3px 6px 14px darkgray;
  }

  #text-report p {
    border: 1px darkgray solid;
    overflow: scroll;
    margin: 10px;
    padding: 5px;
    height: 430px;
  }

  #text-report pre {
    white-space: pre-wrap;
  }

  button {
    margin-left: 10px;
  }

  /* Hide input with copy of report in. Can't set visibility = none or size to 0px */
  #mirror-text-report {
    opacity: 0;
    width: 10px;
  }

</style>
