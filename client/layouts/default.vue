<template>
  <v-app light>
    <v-app-bar
      color="blue"
      fixed
      app
    >
      <nuxt-link id="title" to="/">
        <v-toolbar-title v-text="title"/>
      </nuxt-link>
    </v-app-bar>
    <v-content>
      <v-container>
        <nuxt/>
      </v-container>
    </v-content>
    <v-footer
      app
    >
      <span>&copy; 2019</span>
    </v-footer>
  </v-app>
</template>

<script>
    export default {
        data() {
            return {
                title: 'A For Accessibility'
            }
        }
    }
</script>

<style scoped>
  #title {
    color: white;
    text-decoration: none;
  }
</style>
