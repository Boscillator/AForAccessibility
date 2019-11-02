<template>
  <v-card
    class="mt-4 mx-auto"
    width="75%"
    max-width="800px"
  >
    <v-sheet
      class="v-sheet--offset mx-auto sheet-padding"
      color="blue"
      elevation="12"
      max-width="calc(100% - 32px)"
    >
      <v-sparkline
        ref="sparkline"
        :value="renderedPowBuffer"
        color="white"
        line-width="2"
        auto-draw
      />
    </v-sheet>
    <v-card-title>
      {{message}}
    </v-card-title>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn
        v-if="!isRecording"
        @click="startRecording()"
        color="red"
      >
        <v-icon>mdi-record</v-icon>
      </v-btn>
      <v-btn
        v-else
        @click="stopRecording()"
      >
        <v-icon>mdi-stop</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
    import Recorder from 'recorder-js';

    export default {
        name: "Recorder",
        data: function () {
            return {
                message: "Ready To Record.",
                bufferMaxPoints: 200,
                bufferIndex: 0,
                powBuffer: [],
                renderedPowBuffer: [],
                renderCancelToken: null,
                recorder: null,
                isRecording: false,
            }
        },
        methods: {
            onAnalysed(data) {
                if (this.isRecording) {
                    this.powBuffer.shift();
                    this.powBuffer.push(data.data.reduce((a, b) => a + b));
                }
            },
            renderPowBuffer() {
                this.renderedPowBuffer = this.powBuffer;
            },
            startRecording() {
                if (!this.recorder) {
                    const audioContext = new (window.AudioContext || window.webkitAudioContext)();

                    if (!audioContext) {
                        alert("Your browser does not support web audio.")
                    }

                    this.recorder = new Recorder(audioContext, {
                        onAnalysed: this.onAnalysed
                    });

                    navigator.mediaDevices.getUserMedia({audio: true})
                        .then(stream => {
                            this.recorder.init(stream);
                            this._doStartRecording();
                        })
                        .catch(err => console.log('Uh oh... unable to get stream...', err));
                } else {
                    this._doStartRecording();
                }
            },
            _doStartRecording() {
                this.recorder.start().then(() => this.isRecording = true);
                this.message = "Recording..."
                setInterval(() => this.renderPowBuffer(), 400);
            },
            stopRecording() {
                this.recorder.stop().then(({blob, buffer}) => {
                    this.isRecording = false;
                    this.message = "Done Recording."
                    // Recorder.download(blob, 'my-audio-file');
                    this.$emit('recordingDone', {blob});
                });
            }
        },
        created() {
            this.powBuffer = Array(this.bufferMaxPoints).fill(0);
            this.renderedPowBuffer = Array(this.bufferMaxPoints).fill(0);
        }
    }
</script>

<style scoped>
  .sheet-padding {
    margin-top: 10px;
  }
</style>
