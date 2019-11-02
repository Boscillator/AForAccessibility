<template>
  <v-layout
    column
    justify-center
    align-center
  >
    <Recorder />
  </v-layout>
</template>

<script>
    import Recorder from '~/components/Recorder.vue'
    export default {
        name: "record",
        components: {
            Recorder
        }
    }
</script>

<style scoped>

</style>
