<template>
  <v-layout
    column
    justify-center
    align-center
  >
    <Recorder @recordingDone="onRecorded"/>


    <v-dialog v-model="dialog" persistent max-width="290">
      <v-card>
        <v-card-title class="headline">Use Google's location service?</v-card-title>
        <v-card-text>
          <v-text-field
            v-model="name"
            label="Name"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue" text @click="upload">Upload</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-layout>
</template>

<script>
    import Recorder from '~/components/Recorder.vue'

    export default {
        name: "record",
        components: {
            Recorder
        },
        methods: {
            onRecorded({blob}) {
                this.blob = blob;
                this.dialog = true;
            },
            _getWavBase64() {
                return new Promise((resolve, reject) => {
                    const reader = new FileReader();
                    reader.readAsDataURL(this.blob);
                    reader.onloadend = function() {
                        const base64data = reader.result.slice(22);
                        resolve(base64data);
                    }
                })
            },
            async upload() {
              if(this.name === "") {
                  return;
              }

              let base64 = await this._getWavBase64();

              this.$axios.post('api/upload', {
                  'filename': this.name,
                  'filedata': base64,
                  'timestamp': new Date() / 1000
              }).then(() => this.dialog = false)

            }
        },
        data() {
            return {
                dialog: false,
                blob: null,
                name: ""
            }
        }
    }
</script>

<style scoped>

</style>
