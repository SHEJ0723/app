<template>
  <div class="app-gradient-bg"></div>
  <div id="app-content">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
.app-gradient-bg {
  position: fixed;
  top: 0; left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
  background: linear-gradient(120deg, #a1c4fd 0%, #c2e9fb 50%, #d4a1fd 100%);
  pointer-events: none;
}
#app-content {
  position: relative;
  z-index: 1;
  min-height: 100vh;
}
#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style> 