<template>
  <div class="login">
    <Navbar v-bind:actions="linkActions" msg="Hello"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Navbar from '@/components/Navbar.vue'; // @ is an alias to /src

@Component({
  components: {
    Navbar,
  },
  data: function () {
    return {
      linkActions: [
        {
          title: "Sign Up",
          link: "/signup"
        }
      ]
    }
  }
})
export default class Login extends Vue {}
</script>
