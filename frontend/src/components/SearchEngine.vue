<template>
    <div>
        <form id="search_container">
            <p id="box1">
                <label id="box1" for="">Job Title</label><br />
                <input id="box1" type="text" value="Job Title">
            </p>
            <p id="box2">
                <label id="box2">Location</label><br />
                <input id="box2" value="Location">
            </p>
            <p id="box3">
                <label id="box3">Expected Yearly Income</label><br />
                <input id="box3" value="Expected Yearly Income">
            </p>
            <section>
                <!-- MAKE THIS A BUTTON?? -->
                <input id="search_button" type="button" value="Search">
            </section>
            <p id="box4">
                <label id="box4">Required Skills</label><br />
                <input id="box4" value="Required Skills">
            </p>
            <p id="box5">
                <label id="box5">Years of Experience</label><br />
                <input id="box5" value="Years of Experience">
            </p>
            <p id="box6">
                <label id="box6">Education Level</label><br />
                <input id="box6" value="Education Level">
            </p>
            <p id="box7">
                <label id="box7">Employment Type</label><br />
                <input id="box7" value="Employment Type">
            </p>
        </form>
    </div>
</template>

<script>

</script>

<style>
#search_container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(4, 1fr);
    grid-row-gap: 2%;
    margin-bottom: 3%;
    margin-left: 10%;
    margin-right: 10%;
}

label {
    margin-bottom: 0.5%;
    font-size: 15px;
}

p > input {
    width: 95%;
    height: 80%;
    background-color: #f6f6f6;
    border: #ededed;
    border-width: 3px;
    border-style: solid;
    color: #d3d3d3;
    font-style: italic;
}

#search_button {
    background-color: #245799;
    color: #f0f0f5;
    width: 50%;
    height: 70%;
    border-style: none;
    float: left;
}

section {
    grid-column: 1/2;
    grid-row: 4;
}

#box1 {
    float: left;
    grid-column: 1/2;
    grid-row: 1;
}

#box2 {
    float: left;
    grid-column: 1/2;
    grid-row: 2;
}

#box3 {
    float: left;
    grid-column: 1/2;
    grid-row: 3;
}

#box4 {
    float: left;
    grid-column: 3/4;
    grid-row: 1;
}

#box5 {
    float: left;
    grid-column: 3/4;
    grid-row: 2;
}

#box6 {
    float: left;
    grid-column: 3/4;
    grid-row: 3;
}

#box7 {
    float: left;
    grid-column: 3/4;
    grid-row: 4;
}
</style>
