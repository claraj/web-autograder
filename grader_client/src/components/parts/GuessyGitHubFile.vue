/* If the full file paths were in the config files, this wouldn't be necessary :) */

<template>
<span>
  <a v-if="github_file_url" :href="github_file_url" target="_blank">at github<img src='../../assets/GitHub-Mark-32px.png'></a>
  <a v-else class="github-message">{{message}}</a>
</span>
</template>

<script>

export default {
  name: 'GuessyGitHubFile',
  props: {
    filename: String,
    grade: Number,
  },
  data() {
    return {
      github_file_url: '',
      message: 'looking for file at GitHub...'
    }
  },
  mounted: function() {
    this.$autograder_backend.$guessGithubFileLink(this.grade, this.filename)
      .then(data => {
        this.github_file_url = data.url
        if (!data.url) this.message = ''
      })
      .catch(err => this.message = 'Error finding file at GitHub')
  }
}
</script>

<style>
  span {
    padding-left: 5px;
  }
  .github-message {
    font-style: italic;
  }
  img {
    position: relative;
    top: 5px;
    left: 5px;
    height: 20px;

  }
</style>
