<template>
  <div class="signup">
    <Navbar v-bind:actions='linkActions'></Navbar>
    <section id='signup-section' class='flex-vert'>
      <div class='flex-vert modal-content'>
        <div class='user-img'>
          <img src='/img/add_user_round-dark-empty.png'>
        </div>
        <div v-bind:class='{invalidForm: loginError}' class='form'>
          <input
            autofocus
            id='username'
            name='username'
            pattern='[a-zA-Z0-9_\-]{4,30}'
            placeholder='Username'
            required
            type='text'
            v-model="signupData.username"
            />

          <input
            id='email'
            maxlength=119
            name='email'
            placeholder='Email'
            required
            type='email'
            v-model="signupData.email"
            />

          <input
            id='password'
            name='password'
            pattern='.{4,100}'
            placeholder='Password'
            required
            type='password'
            v-model="signupData.password"
            />

          <button
            type='submit'
            v-on:click="attemptSignup"
            >Login
          </button>
        </div>
        <!-- TODO implement this
          <div>
          <a href='/forgotpassword.html'>Forgot Password?</a>
          </div>
        -->
      </div>
    </section>
  </div>
</template>

<style lang="scss">
#signup-section {
  height: 80%;
}

.signup {
  height: inherit;
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import axios from 'axios';
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
      signupData: {
        username: '',
        email: '',
        password: '',
      },
      loginError: false,
    };
  },
  methods: {
    attemptSignup( event ) {
      console.log( event );
      axios.post('/api/signup', {
        username: this.$data.signupData.username,
        email: this.$data.signupData.email,
        password: this.$data.signupData.password,
      })
        .then((res) => {
          console.log('GOOD RETURN FROM API');
          console.log(res);
          this.$router.push('home');
        })
        .catch( (badRes) => {
          console.log('HELP ME');
          console.log(badRes);
        });
    },
  },
})

export default class Signup extends Vue {}
</script>
