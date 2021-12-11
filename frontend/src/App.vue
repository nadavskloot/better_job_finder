<template>
  <header>
    <h1 id="page_title">Better Job Finder</h1>
  </header>
  <div id="app">
    <SearchEngine />
  </div>
</template>

<script>
import SearchEngine from './components/SearchEngine.vue'

export default {
  name: 'App',
  components: {
    SearchEngine
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
  margin: 0px;
}

#page_title {
  font-weight: 500;
  font-size: 50px;
  margin: 0px;
}
</style>
