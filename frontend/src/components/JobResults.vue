<template>
    <div id="job_results_section">
        <h2 id="results_title">Results</h2>
        <input @click="getSearchResults" type="button" value="Search">
        <ul>
            <li v-for="job in jobs_data" :key="job.id">
                {{job.job_title}} {{job.employer}} {{job.location}} {{job.salary}} {{job.job_post_link}}
            </li>
        </ul>
    </div>
</template>

<script>
    import axios from 'axios'
    
    export default {
        data() {
            return {
                jobs_data: [],
            }
        },
        methods: {
            getSearchResults() {
                const path = 'http://127.0.0.1:5000/getSearchResults'
                axios.get(path).then(response => (this.jobs_data = response.data)).catch(err => {console.log(err)})
                console.log(this.jobs_data)
            }
        }
    }
</script>

<style>
#job_results_section {
    border-top: 1px;
    border-bottom: 0px;
    border-left: 0px;
    border-right: 0px;
    border-style: solid;
    border-color: black;
    height: 100%;
}

#results_title {
    font-weight: 500;
    font-size: 30px;
}
</style>
