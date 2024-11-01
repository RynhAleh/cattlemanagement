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
import cattleTable from './cattleTable.vue';
import cattleSome from './cattleSome.vue';

export default {
  components: {
    cattleTable,
    cattleSome,
  },
  data() {
    return {
    	cMounted: false,
      selectedSection: 'cattleTable', // Компонент по умолчанию
      sections: {
        'cattleTable': 'Список КРС',
        'cattleSome': 'Другой компонент',
        '_': 'Кнопка',
      },
    };
  },
  methods: {
    selectSection(section) {
    	this.cMounted = false;
      this.selectedSection = section; // Прямое присвоение имени компонента
    },
  },
};
</script>
