import Vue from 'vue';
import Router from 'vue-router';
import Login from './views/Login.vue';
import Signup from './views/Signup.vue';
import Home from './views/Home.vue';

Vue.use(Router);

export default new Router({
    routes: [
        // main routes {{{
        {
            path: '/',
            name: 'login',
            component: Login,
        },
        {
          path: '/signup',
          name: 'signup',
          component: Signup,
        },
        {
            path: '/home',
            name: 'home',
            component: Home,
        },
        // main routes }}}
        // redirects {{{
        { path: '/login', redirect: { name: 'login' } },
        {
          path: '/logout',
          redirect: { name: 'login' },
        /*  beforeEnter (pageRedirect, originPage, next) {
            //SOme Stuff will go here. waiting on nick....I think

          }*/
      },
        // redirects }}}
    ],
});
// route level code-splitting
// this generates a separate chunk (about.[hash].js) for this route
// which is lazy-loaded when the route is visited.
// component: () => import(/* webpackChunkName: "about" */ './views/About.vue'),
