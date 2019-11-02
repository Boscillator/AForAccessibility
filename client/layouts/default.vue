<template>
  <v-app light>
    <v-app-bar
      fixed
      app
    >
      <v-toolbar-title v-text="title"/>
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
