<template>
  <v-layout
    column
    justify-center
    align-center
  >
    <h1>Hello World</h1>
    <nuxt-link to="/record">
      <v-btn
        color="blue"
        absolute
        bottom
        right
        fab
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </nuxt-link>
  </v-layout>
</template>

<script>

    export default {
        components: {
        }
    }
</script>
