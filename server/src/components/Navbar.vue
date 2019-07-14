<template>
  <div class="navbar">
    <nav class="gnav nav">
      <img src="/img/logo.png" alt="Logo" class="logo gnav-logo">
      <h2 class="title gnav-title">Inventory</h2>
      <ul class="gnav-actions">
        <template v-for="action in actions">
          <li>
            <router-link v-bind:to="action.link">{{ action.title }}</router-link>
          </li>
        </template>
      </ul>
    </nav>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Navbar extends Vue {
  @Prop() private actions!: Array<{title: string, link: string}>;
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
</style>
