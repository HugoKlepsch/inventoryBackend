<template>
  <div class="signup">
    <Navbar v-bind:actions='linkActions'></Navbar>
    <h1>This is a signup page that will be created soon</h1>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Navbar from '@/components/Navbar.vue'; // @ is an alias to /src

@Component({
  components: {
    Navbar,
  },
  data: () => {
    return {
      linkActions: [
        {
          title: 'Login',
          link: '/login',
        },
      ],
    };
  },
})

export default class Signup extends Vue {}
</script>
