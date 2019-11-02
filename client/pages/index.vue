<template>
  <v-layout
    column
  >
    <h1>Reports</h1>
    <v-card
      class="mx-auto"
      width="75%"
      max-width="800"
    >
      <v-list-item
        v-for="report in reports"
        :key="report.id"
        @click="go(report.id)"
      >
        <v-list-item-content>
          <v-list-item-title>{{report.name}}</v-list-item-title>
        </v-list-item-content>
        <v-list-item-avatar>
          <v-icon>mdi-exit-to-app</v-icon>
        </v-list-item-avatar>
      </v-list-item>
    </v-card>
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
        async asyncData({$axios}) {
            let reportsRequest = await $axios.get('/api/reports');
            let reports = await reportsRequest.data;

            return {
                reports
            }
        },
        methods: {
            go(id) {
              this.$router.push({
                  path:`report/${id}`
              })
            }
        }
    }
</script>
