<template> <!-- {{{ -->
  <div class='login'>
    <Navbar v-bind:actions='linkActions'/>
    <section id='login-section' class='flex-vert'>
      <div class='flex-vert modal-content'>
        <div class='user-img'>
          <img src='/img/face-dark-empty.png'>
        </div>
        <div v-if='isReqsRevealed' id='reqs'>
          <ul>
            <li><em>Username must be between 4 & 30 alphanumeric characters</em></li>
            <li><em>Password must be at least 4 characters</em></li>
          </ul>
        </div>
        <!-- <div class='form'> -->
        <form
          action=""
          v-on:submit="attemptLogin"
          class='form'
          v-bind:class='{invalidForm: loginError}'
          >
          <input
            autofocus
            id='username'
            name='username'
            pattern='[a-zA-Z0-9_\-]{4,30}'
            placeholder='Username'
            required
            type='text'
            v-model="login.username"
            v-on:input.once='revealRequirements'
            />

          <input
            id='password'
            name='password'
            pattern='.{4,100}'
            placeholder='Password'
            required
            type='password'
            v-model="login.password"
            />

          <button
            type='submit'
            v-on:click="attemptLogin"
            >Login
          </button>
        </form>
        <!-- </div> -->
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
  <!-- }}} --></template>


<script lang="ts">
// import Vue from 'vue';
// import Component from 'vue-class-component';
import { Vue, Component } from 'vue-property-decorator';
import Navbar from '@/components/Navbar.vue'; // @ is an alias to /src
import { LinkAction } from '@/interfaces/LinkAction';
import axios from 'axios';

@Component({
  components: { // {{{
    Navbar,
  }, // }}}
})

export default class Login extends Vue {
  // data {{{
  private linkActions: LinkAction[] = [
    {
      title: 'Sign Up',
      link: '/signup',
    },
  ];

  private login: { username: string, password: string } = {
    username: '',
    password: '',
  };

  private isReqsRevealed: boolean = false;
  private loginError: boolean = false;
  // data }}}

  // methods {{{
  private attemptLogin( event: Event ) {
    this.$store.commit( 'setLoginPassword', this.$data.login.password );
    this.$store.commit( 'setLoginUsername', this.$data.login.username );
    this.$store.dispatch( 'postLogin' )
      .then( () => {
        this.$data.loginError = false;
        this.$router.push('home');
      }).catch( () => {
        console.log( 'UNAUTORIZED, see the response below...');
        console.log( this.$store.state.login.response );
        this.$data.loginError = true;
      });
    event.preventDefault();
  }

  private revealRequirements( event: Event ) {
    this.$data.isReqsRevealed = true;
  }
  // methods }}}

}
</script>

<style lang="scss">
#login-section {
  height: 80%;
}

#reqs {
  text-align: left;
}

.login {
  height: inherit;
}
</style>
<<<<<<< a7e63008f072539e976073f03dad1cd984dc956d

=======
>>>>>>> Working on vue logout
