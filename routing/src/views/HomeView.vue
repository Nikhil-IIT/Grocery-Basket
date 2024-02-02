<template>
  <div class="home">
    <div>
      <img alt="Vue logo" src="../assets/logo.jpg" style="margin-left:270px;margin-top:30px;margin-bottom:20px;">
    </div>
    <HelloWorld msg="Welcome to Grocey Store"/>
  </div>
  <footer class="bg-light text-center text-lg-start" style="bottom: 0;width: 100%;height: 60px;">
  <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
    © 2023 Copyright:
      <a class="text-dark" href="#">GroceryStore</a>  
  </div>
</footer>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>
