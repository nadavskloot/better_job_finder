<template>
  <header>
    <h1 id="page_title">Better Job Finder</h1>
  </header>
  <!-- <h1 id="page_title">Better Job Finder</h1> -->
  <div id="app">
    <SearchEngine />
    <JobResults />
  </div>
</template>

<script>
import SearchEngine from './components/SearchEngine.vue'
import JobResults from './components/JobResults.vue'

export default {
  name: 'App',
  components: {
    SearchEngine,
    JobResults
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
  margin: 0px;
}

#page_title {
  font-weight: 500;
  font-size: 50px;
  margin: 0px;
}
</style>
