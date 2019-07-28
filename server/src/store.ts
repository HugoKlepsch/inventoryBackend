import Vue from 'vue';
import Vuex from 'vuex';
import axios from 'axios';

Vue.use( Vuex );

export default new Vuex.Store({
  // Same as 'data' for a Vue component, except accessable by all components.
  state: { // {{{
    login: {
      username: '',
      password: '',
      response: {},
    },
  }, // }}}

  // Mutations commit and track state changes.
  mutations: { // {{{
    setLoginPassword( state, password ) {
      state.login.password = password;
    },
    setLoginResponse( state, response ) {
      state.login.response = response;
    },
    setLoginUsername( state, username ) {
      state.login.username = username;
    },
  }, // }}}

  // Actions update the Vuex state using mutations.
  actions: { // {{{
    postLogin( context ) {
      return new Promise( ( resolve, reject ) => {
        axios.post( '/login', {
          username: context.state.login.username,
          password: context.state.login.password,
        })
          .then( ( res ) => {
            console.log( res );
            context.commit('setLoginResponse', res );
            resolve();
          })
          .catch( ( badRes ) => {
            console.log( badRes );
            context.commit('setLoginResponse', badRes );
            reject();
          });
      });
    },
  }, // }}}

  // Getters access the state for various slices or filters of data.
  getters: { // {{{

  }, // }}}
});
