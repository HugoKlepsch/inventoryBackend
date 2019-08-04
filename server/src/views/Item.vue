<template>
  <!-- {{{ -->
  <div class="item">
    <Navbar v-bind:actions='linkActions'></Navbar>
    <div class="card">
      <div class="vert-stack">
        <div class="card-title">
          <h1>Item</h1>
          <h1>#24</h1>
        </div>
        <p class="desc">Ipsum sit quasi eligendi non tenetur Reprehenderit iste aspernatur dolore commodi consequuntur nesciunt Nesciunt voluptate aperiam quis veniam provident Nobis pariatur mollitia unde ab in. Accusantium commodi molestias alias animi</p>
      </div>
      <div class="vert-stack">
        <dl>
          <dt>Purchased:</dt>
          <dd>5.00 ~ <em>2019-07-15</em></dd>
          <dt>Listed:</dt>
          <dd>$6.00 ~ <em>2019-08-03</em></dd>
          <dt>Sold:</dt>
          <dd> -- </em></dd>
        </dl>
      </div>
      <div class="vert-stack">
        <div class="fake-image"></div>
      </div>
    </div>
  </div>
  <!-- }}} -->
</template>


<script lang="ts"> /*{{{*/
import { Vue, Component } from 'vue-property-decorator';
import Navbar from '@/components/Navbar.vue';
import { LinkAction } from '@/interfaces/LinkAction';

@Component({
  components: {
    Navbar,
  },
})

export default class Item extends Vue {
  // data {{{
  private linkActions: LinkAction[] = [
    { title: 'Home', link: '/home' },
    { title: 'Log Out', link: '/logout' },
  ];
  // data }}}


  // methods {{{

  // methods }}}
}
  /*}}}*/ </script>


<style scoped lang="scss">

h1 {
  margin: 0em 0.5em 0em 0em;
}

dl {
  margin-top: 4rem;
}

div.card {
  width: 95%;
  height: 80vh;
  background-color: #121212;
  margin-left: 2.5%;
  margin-top: 5vh;
  align-content: flex-start;
  align-items: flex-start;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-around;
}

p.desc {
  width: 400px;
}

.card-title {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;

}

.fake-image {
  min-width: 300px;
  min-height: 200px;
  background-color: red;
}

.vert-stack {
  display: flex;
  flex-flow: wrap column;
  /*
  align-content: flex-start;
  align-items: center;
  justify-content: center;
  */
}
</style>

