<template>
  <q-layout view="hHh lpR lFf">

    <q-header reveal elevated class="bg-dark text-white">
      <q-toolbar>
        <q-btn dense flat round icon="menu" @click="left = !left" />

        <q-toolbar-title>
          <q-avatar>
            <img src="~assets/quasar-logo-full.svg">
          </q-avatar>
          {{ product }} v{{ version }}
        </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="left" side="left" elevated>
      <!-- drawer content -->
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <q-footer reveal bordered class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="~assets/quasar-logo-full.svg">
          </q-avatar>
          {{ product }}
        </q-toolbar-title>
      </q-toolbar>
    </q-footer>

  </q-layout>
</template>

<script>
export default {
  data () {
    return {
      left: false,
      version: process.env.VERSION,
      product: process.env.PRODUCT
    }
  },
  mounted () {
    console.log(process.env)
  }
}
</script>
