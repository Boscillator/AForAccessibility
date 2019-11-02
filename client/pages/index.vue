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
    import Logo from '~/components/Logo.vue'
    import VuetifyLogo from '~/components/VuetifyLogo.vue'

    export default {
        components: {
            Logo,
            VuetifyLogo
        }
    }
</script>
