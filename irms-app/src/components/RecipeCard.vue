<template>
    <div>
        <h2>{{ recipe.title }}</h2>
        <p>{{ recipe.description }}</p>
    </div>

</template>

<script>
    export default {
        props: ['recipe']
    };
</script>