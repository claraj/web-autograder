/* If the full file paths were in the config files, this wouldn't be necessary :) */

<template>

  <a v-if="github_file_url" :href="github_file_url">at github</a>
  <a v-else class="github-message">{{message}}</a>

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
      message: 'loading link to GitHub'
    }
  },
  mounted: function() {
    this.$autograder_backend.$guessGithubFileLink(this.grade, this.filename)
      .then(data => {
        this.github_file_url = data.url
        if (!data.url) this.message = 'Couldn\'t find file at GitHub'
      })
      .catch(err => this.message = 'Error finding at GitHub')
  }
}
</script>

<style>
  .github-message {
    font-style: italic;
  }
</style>
