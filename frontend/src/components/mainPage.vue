<template>
  <div id="main-page">
    <div id="left-bar">
      <h2 id="caption">Учет КРС 1.0</h2>
      <ul>
        <li v-for="(value, key) in sections"
          :key="key"
          :class="{ selected: selectedSection === key }"
          @click="selectSection(key)">
          {{ value }}
        </li>
      </ul>
    </div>

    <div id="right-bar">
      <component :is="selectedSection" />
    </div>
  </div>
</template>


<script>
import cattleHeader from './cattle/cattleHeader.vue';
import milkingHeader from './milking/milkingHeader.vue';
import feedingHeader from './feeding/feedingHeader.vue';
import insemHeader from './insem/insemHeader.vue';
import movingHeader from './moving/movingHeader.vue';
import treatHeader from './treat/treatHeader.vue';
import comingHeader from './coming/comingHeader.vue';
import exitHeader from './exit/exitHeader.vue';
import dictsHeader from './dicts/dictsHeader.vue';

export default {
  components: {
    cattleHeader,
    milkingHeader,
    feedingHeader,
    insemHeader,
    movingHeader,
    treatHeader,
    comingHeader,
    exitHeader,
    dictsHeader,
  },
  data() {
    return {
      selectedSection: 'cattleHeader', // Компонент по умолчанию
      sections: {
        'cattleHeader': 'Список КРС',
        'milkingHeader': 'Доение',
        'feedingHeader': 'Кормление',
        'insemHeader': 'Осеменение',
        'movingHeader': 'Перемещение',
        'treatHeader': 'Лечение',
        'comingHeader': 'Приход',
        'exitHeader': 'Расход',
        'dictsHeader': 'Справочники',
      },
    };
  },

  methods: {
    selectSection(section) {
      this.selectedSection = section; // Прямое присвоение имени компонента
    },
  },
};
</script>
