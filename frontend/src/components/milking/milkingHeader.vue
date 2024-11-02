<template>
  <div id="header">
		<ul>
			<li v-for="(value, key) in sections"
				:key="key"
				:class="{ selected: selectedSection === key }"
				@click="selectSection(key)">
				{{ value }}
			</li>
		</ul>
	</div>
	<div :hidden="!cMounted"  class="content">
		<div class="common-container">
			<component :is="selectedSection" @child-mounted="cMounted = true"></component>
		</div>
	</div>
</template>

<script>
import milkingTable from './milkingTable.vue';
import milkingSome from './milkingSome.vue';

export default {
  components: {
    milkingTable,
    milkingSome,
  },
  data() {
    return {
    	cMounted: false,
      selectedSection: 'milkingTable',
      sections: {
        'milkingTable': 'Журнал доения',
        'milkingSome': 'Отчет по надоям',
      },
    };
  },
  methods: {
    selectSection(section) {
    	this.cMounted = false;
      this.selectedSection = section;
    },
  },
};
</script>
