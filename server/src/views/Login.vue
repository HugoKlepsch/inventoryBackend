<template>
  <div class='login'>
    <Navbar v-bind:actions='linkActions' msg='Hello'/>
    <section class='flex-vert'>
      <div class='flex-vert modal-content'>
        <div class='user-img'>
          <img src='/img/face.png'>
        </div>
        <div class='form-input flex-vert'>
          <form id='login form' action='/login' method='post'>
            <div class='form-group'>
              <input id='username' type='text' name='username' class='form-control' placeholder='Username'
                     required pattern='[a-zA-Z0-9_\-]{4,30}' autofocus>
            </div>
            <div class='form-group'>
              <input id='password' type='password' name='password' class='form-control' placeholder='Password'
                     required pattern='.{4,100}'>
            </div>

            <button type='submit' class='btn btn-primary' onclick='login();'>Login</button>
          </form>
        </div>
        <!-- TODO implement this
          <div>
          <a href='/forgotpassword.html'>Forgot Password?</a>
          </div>
        -->
        <div class='center'>
          <a href='/signup.html'>Sign up</a>
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
})
export default class Login extends Vue {}
</script>
