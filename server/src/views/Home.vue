<!--
  2019-07-14 ~~ Waiting for the API to catch up so that we can send a request to /getSales or something and retrueve a list of items to display in the table.
  This page is navigable on the Node.js dev server at the url http://localhost:8080/#/home .
-->
<template>
  <div>
    <Navbar v-bind:actions="linkActions"/>
    <p>This is the main user page!</p>
    <section class="grid">
      <div class="block-sales flex-vert">
        <strong>Sales this Month</strong>
        <table>
          <tr>
            <th v-for="header in salesTable.headers">{{ header }}</th>
          </tr>
          <template v-for="itemObj in salesTable.defaultItems">
            <tr>
              <td>{{ itemObj.item }}</td>
              <td>{{ itemObj.buyPrice }}</td>
              <td>{{ itemObj.sellPrice }}</td>
            </tr>
          </template>
        </table>
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
  data: () => { // {{{
    return {
      linkActions: [
        {
          title: 'Log Out',
          link: '/logout',
        },
      ],
      salesTable: {
        headers: [ 'Item', 'Buy Price', 'Sell Price' ],
        defaultItems: [
          { item: 'Thing1', buyPrice: '$100', sellPrice: '$120' },
          { item: 'Anotha One', buyPrice: '$6.99', sellPrice: '$101.50' },
        ],
      },
    };
  }, // }}}
})
export default class Home extends Vue {}
</script>


<style lang="scss">
</style>
