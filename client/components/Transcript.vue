<template>
  <v-card
    class="card-padding"
  >
    <v-sheet
      class="v-sheet--offset mx-auto sheet-padding transcript"
      elevation="0"
      height="100%"
      max-width="calc(100% - 32px)"
    >
      <!--{{section.body}}-->
      <div v-for="item in section.body">
        <h3>Speaker #{{item.key}}</h3>
        {{item.sentence}}
        <br>
      </div>
    </v-sheet>
    <v-card-title class="title">{{section.title}}</v-card-title>
  </v-card>
</template>

<script>
    export default {
        name: "Transcript",
        props: ['section']
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

  .transcript {
    overflow-y: scroll;
    max-height: 400px;
    padding-left: 10px;
    padding-top: 10px;
    margin-bottom: 40px;
  }

</style>
