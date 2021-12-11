<template>
    <div id="search_div">
        <form id="search_container">
            <div id="left">
                <label>Desired Job Title</label>
                <input v-model="search_data.job_title" type="text" placeholder="'Software Engineer, Financial Manager, etc.'">

                <label>Your Years of Experience</label>
                <input class="range_input" v-model="search_data.experience" type="range" min="0" max="50">

                <label>Your Education Level</label>
                <select v-model="search_data.education">
                    <option>High School</option>
                    <option>Bachelors</option>
                    <option>Masters</option>
                    <option>P.H.D.</option>
                </select>

                <label>Your Skills</label>
                <input v-model="search_data.required_skills" type="text" placeholder="Ex.: 'Java, Microsoft Office, etc.'">
            </div>
            <div id="right">
                <label>Location</label>
                <input v-model="search_data.location" type="text" placeholder="Location">

                <label>Expected Yearly Income</label>
                <input class="range_input" v-model="search_data.income" type="range" min="0" max="500,000">

                <label>Employment Type</label>
                <select v-model="search_data.job_type">
                    <option>Full-time</option>
                    <option>Part-time</option>
                    <option>Internship</option>
                    <option>Contract</option>
                </select>

                <label>Find your dream job!</label>
                <input id="search_button" @click="getSearchResults" type="button" value="Search">
            </div>
        </form>
    </div>
    <div id="job_results_section">
        <h2 id="results_title">Results</h2>
        <ul>
            <li v-for="job in jobs_data" :key="job.id">
                {{job.job_title}} {{job.employer}} {{job.job_post_link}}
            </li>
        </ul>
    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        data() {
            return {
                search_data: {
                    job_title: "",
                    location: "",
                    income: null,
                    key_words: "",
                    required_skills: "",
                    experience: null,
                    education: "",
                    job_type: ""
                },
                jobs_data: []
            }
        },
        methods: {
            getSearchResults() {
                const path = 'http://127.0.0.1:5000/getSearchResults'
                axios.post(path, {
                    job_title: this.search_data.job_title,
                    location: this.search_data.location,
                    income: this.search_data.income,
                    key_words: this.search_data.key_words,
                    required_skills: this.search_data.required_skills,
                    experience: this.search_data.experience,
                    education: this.search_data.education,
                    job_type: this.search_data.job_type
                })
                .then(response => {console.log(response)})
                .catch(err => {console.log(err)})

                axios.get(path).then(response => (this.jobs_data = response.data)).catch(err => {console.log(err)})
                console.log(this.jobs_data)
            }
        }
    }
</script>

<style>
#search_div {
    height: 400px;
    margin-bottom: 1%;
}

#search_container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: 1fr, 1fr;
    grid-column-gap: 9%;
    margin-left: 13%;
    margin-right: 13%;
    height: 100%;
}

#left {
    grid-column: 1/2;
    grid-row: 1;
}

#right {
    grid-column: 2/3;
    grid-row: 1;
}

label {
    float: left;
    margin-bottom: 0.5%;
    font-size: 15px;
    margin-top: 3%;
}

::placeholder {
    color: #d3d3d3;
    font-style: italic;
}

input, select {
    float: left;
    width: calc(100% - 10px);
    height: 11%;
    background-color: #f6f6f6;
    border: #ededed;
    border-width: 3px;
    border-style: solid;
}

select {
    height: 12.5%;
    width: 100%;
}

.range_input {
    background-color: red;
    height: 11%;
    width: 100%;
    padding-top: 1px;
    padding-bottom: 1px;
    margin: 0px;
}

#search_button {
    background-color: #245799;
    color: #f0f0f5;
    width: 100%;
    height: 13%;
    border-style: none;
    grid-column: 1/3;
    grid-row: 2;
    align-self: end;
    justify-self: center;
    font-size: 15px;
}

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
