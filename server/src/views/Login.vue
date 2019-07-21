<template>
  <div class='login'>
    <Navbar v-bind:actions='linkActions'/>
    <section id='login-section' class='flex-vert'>
      <div class='flex-vert modal-content'>
        <div class='user-img'>
          <img src='/img/face-dark-empty.png'>
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
            v-model="username"
            />

          <input
            id='password'
            name='password'
            pattern='.{4,100}'
            placeholder='Password'
            required
            type='password'
            v-model="password"
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


<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import Navbar from '@/components/Navbar.vue'; // @ is an alias to /src

@Component({
  components: {
    Navbar,
  },
  computed: {
    password: {
      get() {
        return this.$store.state.login.password;
      },
      set( value ) {
        this.$store.commit( 'setLoginPassword', value );
      },
    },
    username: {
      get() {
        return this.$store.state.login.username;
      },
      set( value ) {
        this.$store.commit( 'setLoginUsername', value );
      },
    },
  },
  data: () => {
    return {
      linkActions: [
        {
          title: 'Sign Up',
          link: '/signup',
        },
      ],
    };
  },
  methods: {
    attemptLogin( event ) {
      console.log( event );
      this.$store.dispatch( 'postLogin' )
        .then( () => {
          this.$router.push('home');
        }).catch( () => {
          console.log( 'UNAUTORIZED, see the response below...');
          console.log( this.$store.state.login.response );
        });
    },
  },
})
export default class Login extends Vue {}
</script>

<style lang="scss">
#login-section {
  height: 80%;
}

.login {
  height: inherit;
}
</style>

