<template>
    <div id="home">
        <div id="search_div">
            <form id="search_container">
                <div id="left">
                    <label>Desired Job Title</label>
                    <input
                        v-model="search_data.job_title"
                        type="text"
                        placeholder="'Software Engineer, Financial Manager, etc.'"
                    />

                    <label
                        v-html="
                            'Your Years of Experience < <b style=\'color:#61ba46\'>' +
                            search_data.experience +
                            ' years</b>'
                        "
                    ></label>
                    <input
                        class="range_input"
                        v-model="search_data.experience"
                        type="range"
                        min="0"
                        max="60"
                    />

                    <label>Your Education Level</label>
                    <select v-model="search_data.education">
                        <option>High School</option>
                        <option>Bachelors</option>
                        <option>Masters</option>
                        <option>P.H.D.</option>
                    </select>

                    <label>Your Skills</label>
                    <input
                        v-model="search_data.required_skills"
                        type="text"
                        placeholder="Ex.: 'Java, Microsoft Office, etc.'"
                    />
                </div>
                <div id="right">
                    <label>Location</label>
                    <input
                        v-model="search_data.location"
                        type="text"
                        placeholder="Location"
                    />

                    <label
                        >Expected Yearly Income >
                        <b style="color: #61ba46"
                            >${{ search_data.income }}</b
                        ></label
                    >
                    <input
                        class="range_input"
                        v-model="search_data.income"
                        type="range"
                        min="0"
                        max="500000"
                    />

                    <label>Employment Type</label>
                    <select v-model="search_data.job_type">
                        <option>Full-time</option>
                        <option>Part-time</option>
                        <option>Internship</option>
                        <option>Contract</option>
                    </select>

                    <label>Find your dream job!</label>
                    <input
                        id="search_button"
                        @click="getSearchResults"
                        type="button"
                        value="Search"
                    />
                </div>
            </form>
        </div>
        <div id="job_results_section">
            <h2 id="results_title">Results</h2>
            <table id="job_results_table" v-if="jobs_data.length > 0">
                <thead>
                    <tr>
                        <th class="job_title_header">Job Title</th>
                        <th class="employer_header">Company</th>
                        <th class="location_header">Location</th>
                        <th class="years_experience_header">
                            Years Experience
                        </th>
                        <th class="education_level_header">Education Level</th>
                        <th class="employment_type_header">Employment Type</th>
                        <th class="required_skills_header">Required Skills</th>
                        <th class="salary_header">Salary</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="job in jobs_data" :key="job.id">
                        <td class="job_title_column">
                            <a :href="job.job_post_link" target="_blank">{{
                                job.job_title
                            }}</a>
                        </td>
                        <td class="employer_column">
                            {{ job.employer }}
                        </td>
                        <td class="location_column">
                            {{ job.location }}
                        </td>
                        <td class="years_experience_column">
                            {{ job.years_experience }}
                        </td>
                        <td class="education_level_column">
                            {{ job.education_level }}
                        </td>
                        <td class="employment_type_column">
                            {{ job.employment_type }}
                        </td>
                        <td class="required_skills_column">
                            {{ job.required_skills }}
                        </td>
                        <td class="salary_column">
                            {{ job.salary }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <!-- If reults are taking a long time to fetch, this will display to let the user know -->
        <div :style="{ display: response_waiting }" id="response_waiting_alert">
            <div>
                Sorry! We understand that this isn't ideal but, this site is
                still early in it's development so your query may take upto
                <b>2 minutes</b> to get a response. Please wait patiently until
                this alert disappears.
                <img
                    style="
                        height: 50px;
                        width: 50px;
                        margin: 0 auto;
                        display: block;
                    "
                    src="https://i.stack.imgur.com/kOnzy.gif"
                />
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            search_data: {
                job_title: "",
                location: "",
                income: 0,
                key_words: "",
                required_skills: "",
                experience: 0,
                education: "",
                job_type: "",
            },
            jobs_data: [],
            response_waiting: "none",
        };
    },
    methods: {
        // Executes POST request to send user search input to backend, then
        // executes GET request to grab the job results from Flask database
        // and populates an HTML table with said results
        // Utilizes axios (a Vue.js wrapper for AJAX) to load the results
        // without refreshing the page
        getSearchResults() {
            const path = "http://127.0.0.1:5000/getSearchResults";
            this.response_waiting = "block";
            axios
                .post(path, {
                    job_title: this.search_data.job_title,
                    location: this.search_data.location,
                    income: this.search_data.income,
                    key_words: this.search_data.key_words,
                    required_skills: this.search_data.required_skills,
                    experience: this.search_data.experience,
                    education: this.search_data.education,
                    job_type: this.search_data.job_type,
                })
                .then((response) => {
                    this.jobs_data = response.data;
                    this.response_waiting = "none";
                    console.log(response);
                })
                .catch((err) => {
                    console.log(err);
                    this.response_waiting = "none";
                });
        },
    },
};
</script>

<style>
#home {
    flex: 1;
    min-height: 0px;
    display: flex;
    flex-direction: column;
}

#search_div {
    height: 40%;
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

input,
select {
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
    min-height: 0;
    flex: 1;
    display: flex;
    flex-direction: column;
}

#results_title {
    font-weight: 500;
    font-size: 30px;
}

#job_results_table {
    flex: 1;
    overflow: scroll;
    display: block;
    border-collapse: collapse;
    padding: 0px 20px;
    width: fit-content;
    max-width: 100%;
    margin: 0px auto;
}
#job_results_table > thead {
    position: sticky;
    top: 0;
}
#job_results_table th,
#job_results_table td {
    white-space: nowrap;
    text-align: left;

    padding: 10px 20px 10px 0;
}
#job_results_table th {
    background-color: white;
}
#job_results_table td {
    background-color: white;
    border-top: 1px solid #cfcfcf;
    font-size: 0.8em;
}

.job_title_column > a {
    text-decoration: none;
    font-weight: bold;
    color: #227aec;
}

#response_waiting_alert {
    position: fixed;
    top: 0px;
    left: 0px;
    right: 0px;
    bottom: 0px;
    background-color: rgba(0, 0, 0, 0.2);
}

#response_waiting_alert > div {
    position: fixed;
    width: 400px;
    padding: 30px;
    background-color: rgb(238, 251, 253);
    box-shadow: 0px 0px 50px rgba(0, 0, 0.2, 0.5);
    border-radius: 10px;
    margin: auto;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
</style>
