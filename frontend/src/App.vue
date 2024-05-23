<template>
  <div id="app">
    <NumToEnglish />
  </div>
</template>

<script>
import NumToEnglish from './components/NumToEnglish.vue';

export default {
  name: 'App',
  components: {
    NumToEnglish
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>