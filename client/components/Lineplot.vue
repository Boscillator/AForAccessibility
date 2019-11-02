<template>
  <v-card
    class="card-padding"
  >
    <v-sheet
      class="v-sheet--offset mx-auto sheet-padding"
      elevation="0"
      max-width="calc(100% - 32px)"
    >
      <Chart :options="section.options"/>
    </v-sheet>
  </v-card>
</template>

<script>

    import {Chart} from 'highcharts-vue'
    export default {
        name: "Lineplot",
        components: {
            Chart
        },
        props: ['section'],
        created() {
          if(!this.section.options.title) {
              this.section.options.title = {
                  text: this.section.title
              }
          }
        }
    }
</script>

<style scoped>

  .card-padding {
    width: 100%;
    height: 100%;
  }
  .sheet-padding {
    margin-top: 40px;
  }
  .big-text {
    font-size: 75pt;
    padding-left: 25px;
    font-weight: bold;
  }
</style>
