<template>
  <v-card
    class="card-padding"
  >
    <v-sheet
      class="v-sheet--offset mx-auto sheet-padding big-text"
      elevation="0"
      height="85%"
      max-width="calc(100% - 32px)"
    >
      {{section.body}}
    </v-sheet>
    <div v-if="section.tip" class="tip">{{section.tip}}</div>
    <v-card-title class="title">{{section.title}}</v-card-title>
  </v-card>
</template>

<script>
    export default {
        name: "BigText",
        props: [
            "section"
        ]
    }
</script>

<style scoped>
  .card-padding {
    margin-right: 0 !important;
    width: 100%;
    height: 100%;
  }
  .sheet-padding {
    margin-top: 40px;
  }
  .title {
    position: absolute;
    bottom: 0px;
  }
  .tip {
    position: absolute;
    bottom: 32pt;
    padding-left: 15px;
  }
  .big-text {
    font-size: 75px;
    font-weight: bold;
    font-color: #555;
  }
</style>
