<template>
  <v-progress-circular
    class="loading"
    v-if="!report"
    indeterminate
    color="blue"
    size="200"
    width="25"
  />

  <div v-else id="report-grid">
    <div
      class="report-section"
      :class="{wide: section.wide}"
      v-for="section in report">
      <BigText :section="section" v-if="section.type == 'bigtext'" :key="section.title"/>
      <Transcript :section="section" v-if="section.type == 'transcript'" :key="section.title"/>
      <Lineplot :section="section" v-if="section.type == 'highchart'" :key="section.title"/>
    </div>
  </div>
</template>

<script>
    import BigText from "../../components/BigText";
    import Lineplot from "../../components/Lineplot";
    import Transcript from "../../components/Transcript";

    export default {
        components: {Lineplot, BigText, Transcript},
        methods: {
            async refreshReport() {
                console.log("Refresh");
                if (!this.report) {
                    try {
                        let reportRequest = await this.$axios.get(`/api/report/${this.$route.params.id}`);
                        let report = await reportRequest.data;
                        this.report = report;
                    } catch {
                        setTimeout(() => this.refreshReport(), 1000);
                    }
                }
            }
        },
        mounted() {
            if(this.report == null) {
                this.refreshReport();
            }
        },
        async asyncData({params, $axios}) {
            try {
                let reportRequest = await $axios.get(`/api/report/${params.id}`);
                let report = await reportRequest.data;
                return {
                    report
                }
            } catch {
                return {
                    report: null
                }
            }
        }
    }
</script>

<style scoped>
  #report-grid {
    width: 100%;
    margin-bottom: 40px;

    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-column-gap: 25px;
    grid-row-gap: 25px;
    justify-items: center;
    align-items: center;
  }

  .loading {
    margin: auto;
    width: 200px;
    display: block;
  }

  .report-section {
    width: 100%;
    height: 100%;
  }

  @media (min-width: 720px) {
    .wide {
      grid-column: 1/span 2;
    }
  }

  @media (max-width: 720px) {
    #report-grid {
      grid-template-columns: repeat(1, 1fr);
    }

  }

</style>
