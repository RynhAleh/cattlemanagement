<template>
  <div>
    ЗДЕСЬ БУДЕТ ОТЧЕТ ПО СКОТУ
  </div>
</template>

<script>

export default {
	watch: {
		iMounted(n, o) {if(n && this.cMounted) this.$emit("child-mounted");},
		cMounted(n, o) {if(n && this.iMounted) this.$emit("child-mounted");},
	},
  data() {
    return {
    	iMounted: false,
    	cMounted: false,
    };
  },
	mounted() {
		this.iMounted = true;
        this.cMounted = true;
  },
};
</script>     