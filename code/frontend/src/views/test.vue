<template>
    <div>
        <h2> Test Page</h2>
        <form action="">
            <label for="text">Enter your message:</label>
            <input type="text" name="text" id="" v-model="this.message"><br><br>
            <button type="submit" @click.prevent=" this.testMethod()"> Submit</button>
        </form>
        {{ text }}
    </div>
</template>

<script>
import axios from 'axios'

export default {
    neme: 'testRoute',
    data() {
        return{
            text: '',
            message:'Hello Vue!'
        }
    },
    methods: {
        testMethod() {
            console.log('trying to call a method and print a var: ', this.message)
        }
    }
}
</script>

<style> </style>