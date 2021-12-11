<template>
    <div id="search_div">
        <form id="search_container">
            <div id="left">
                <label>Desired Job Title</label>
                <input v-model="search_data.job_title" type="text" placeholder="Desired Job Title">

                <label>Location</label>
                <input v-model="search_data.location" type="text" placeholder="Location">

                <label>Expected Yearly Income</label>
                <input v-model="search_data.income" type="text" placeholder="Expected Yearly Income">

                <label>Employment Type</label>
                <input v-model="search_data.job_type" type="text" placeholder="Employment Type">
            </div>
            <div id="right">
                <label>Your Skills</label>
                <input v-model="search_data.required_skills" type="text" placeholder="Your Skills">

                <label>Your Years of Experience</label>
                <input v-model="search_data.experience" type="text" placeholder="Your Years of Experience">

                <label>Your Education Level</label>
                <input v-model="search_data.education" type="text" placeholder="Your Education Level">

                <label>Find your dream job!</label>
                <input id="search_button" @click="search" type="button" value="Search">
            </div>
        </form>
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
                    income: "",
                    key_words: "",
                    required_skills: "",
                    experience: "",
                    education: "",
                    job_type: ""
                }
            }
        },
        methods: {
            search() {
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
    grid-column-gap: 10%;
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

input {
    float: left;
    width: calc(100% - 10px);
    height: 11%;
    background-color: #f6f6f6;
    border: #ededed;
    border-width: 3px;
    border-style: solid;
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
</style>
