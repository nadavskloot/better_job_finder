<template>
    <div id="search_div">
        <form id="search_container">
            <div id="left">
                <label class="box1">Job Title</label>
                <input class="box1" type="text" placeholder="Job Title">

                <label class="box2">Location</label>
                <input class="box2" type="text" placeholder="Location">

                <label class="box3">Expected Yearly Income</label>
                <input class="box3" type="text" placeholder="Expected Yearly Income">

                <label class="box4">Key Words</label>
                <input class="box4" type="text" placeholder="Key Words">
            </div>
            <div id="right">
                <label class="box5">Required Skills</label>
                <input class="box5" type="text" placeholder="Required Skills">

                <label class="box6">Years of Experience</label>
                <input class="box6" type="text" placeholder="Years of Experience">

                <label class="box7">Education Level</label>
                <input class="box7" type="text" placeholder="Education Level">

                <label class="box8">Employment Type</label>
                <input class="box8" type="text" placeholder="Employment Type">
            </div>
            <input id="search_button" @click="search" type="button" value="Search">
        </form>
    </div>
</template>

<script>
    export default {
        methods: {
            search() {
                
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
    width: 100%;
    height: 12%;
    background-color: #f6f6f6;
    border: #ededed;
    border-width: 3px;
    border-style: solid;
}

#search_button {
    background-color: #245799;
    color: #f0f0f5;
    width: 28%;
    height: 60%;
    border-style: none;
    grid-column: 1/3;
    grid-row: 2;
    align-self: end;
    justify-self: center;
    font-size: 15px;
}
</style>
