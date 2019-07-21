<template>
  <div class='login'>
    <Navbar v-bind:actions='linkActions'/>
    <section id='login-section' class='flex-vert'>
      <div class='flex-vert modal-content'>
        <div class='user-img'>
          <img src='/img/face-dark-empty.png'>
        </div>
        <div class='form'>
          <input
            autofocus
            id='username'
            name='username'
            pattern='[a-zA-Z0-9_\-]{4,30}'
            placeholder='Username'
            required
            type='text'
            v-model="loginData.username"
            />

          <input
            id='password'
            name='password'
            pattern='.{4,100}'
            placeholder='Password'
            required
            type='password'
            v-model="loginData.password"
            />

          <button
            type='submit'
            v-on:click="attemptLogin"
            >Login
          </button>
        </div>
        <!-- TODO implement this
          <div>
          <a href='/forgotpassword.html'>Forgot Password?</a>
          </div>
        -->
        <div class='center'>
          <router-link to="/signup">Sign up</router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style lang="scss">
#login-section {
  height: 80%;
}

.login {
  height: inherit;
}
</style>

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
          title: 'Sign Up',
          link: '/signup',
        },
      ],
      loginData: {
        username: '',
        password: '',
      },
    };
  },
  methods: {
    attemptLogin( event ) {
      console.log( event );
      this.$http.post('/login', {
        username: this.$data.loginData.username,
        password: this.$data.loginData.password,
      }).then((res) => {
        console.log('GOOD RETURN FROM API');
        console.log(res);
        this.$router.push('home');
      }, (badRes) => {
        console.log('HELP ME');
        console.log(badRes);
      });
    },
  },
})
export default class Login extends Vue {}
</script>
