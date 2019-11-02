<template>
  <div id="report-grid">
    <div
      class="report-section"
      :class="{wide: section.wide}"
      v-for="section in report">
      <BigText :section="section" v-if="section.type == 'bigtext'" :key="section.title"/>
      <Lineplot :section="section" v-if="section.type == 'highchart'" :key="section.title"/>
    </div>
  </div>
</template>

<script>
    import BigText from "../../components/BigText";
    import Lineplot from "../../components/Lineplot";
    export default {
        components: {Lineplot, BigText},
        async asyncData({params}) {
            return {
                report: [
                    {
                        "type": "highchart",
                        "wide": "true",
                        "title": "Words Per Minute",
                        "options": {
                            "series": [{
                                "data": [1,2,3]
                            }]
                        }
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Clarity",
                        "body": "B-"
                    },
                    {
                        "type": "bigtext",
                        "title": "Accessibility",
                        "body": "C"
                    },
                ]
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

  .report-section {
    width: 100%;
    height: 100%;
  }

  .wide {
    grid-column: 1/span 2;
  }

  @media (max-width: 720px) {
    #report-grid {
      grid-template-columns: repeat(1, 1fr);
    }

  }

</style>
