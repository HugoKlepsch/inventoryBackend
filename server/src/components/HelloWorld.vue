<template>
  <div class="hello">
    <nav class="gnav nav">
      <img src="/img/logo.png" alt="Logo" class="logo gnav-logo">
      <h2 class="title gnav-title">Inventory</h2>
      <ul class="gnav-actions">
        <li><a href="/signup">Sign Up</a></li>
      </ul>
    </nav>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class HelloWorld extends Vue {
  @Prop() private msg!: string;
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
