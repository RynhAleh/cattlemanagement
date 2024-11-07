<template>
	<div v-if="status > 0" class="table-container" style="min-width: 800px; max-width: 1500px;">
		<baseTable :data="itemsWithClasses" :columns="tableColumns" :status="status" :table="table" @child-mounted="cMounted = true" @update-data="() => loadData(table, true)"/><!--child1-->
	</div>
</template>

<script>
import baseTable from '../baseTable.vue';
import dataLoader from '@/utils/dataLoader';

export default {
	watch: {
		iMounted(n, o) {if(n && this.cMounted) this.$emit("child-mounted");},
		cMounted(n, o) {if(n && this.iMounted) this.$emit("child-mounted");},
    table(newTable) {this.loadData(newTable);},
	},
  components: {
    baseTable,
  },
  data() {
    return {
    	iMounted: false,
    	cMounted: false,
    	table: 'cattle',
    	status: 0,
      tableData: [], // Начальное состояние пустое
      limit: 20, // Загрузим 1000 записей при первой загрузке
      offset: 0,
      tableColumns: [
        { key: 'id', label: 'ID', type: 'number' },
        { key: 'name', label: 'Имя или инд.номер', type: 'string' },
        { key: 'color', label: 'Цвет/окрас, лет', type: 'string' },
        { key: 'breed', label: 'Порода', type: 'string' },
        { key: 'birthdate', label: 'Дата рождения', type: 'date' },
      ],
			ref: (() => {const date = new Date(); date.setDate(date.getDate() - 365*3); return date;})(),  // тек.дата - 3г
    };
  },
	mounted() {
    this.loadData(this.table);
		this.iMounted = true;
  },
  computed: {
    itemsWithClasses() {
      return this.tableData.map(item => {
        const dictClass = {};
				const dt = new Date(item.birthdate);

        // Условия для классов
        if (dt < this.ref) dictClass["_"] = "disabled";
        if (item.color === 'рыжая') dictClass["color"] = "warning";
        if (item.id % 7 === 0) dictClass["id"] = "info";
        if (dt.getMonth() === 6) dictClass["birthdate"] = "success";
        if (item.id % 3 === 0) dictClass["id"] = "success";
        if (item.id % 7 === 0) dictClass["id"] = "disabled";


        return {
          ...item,
          dictClass: dictClass,
        };
      });
    }
  },
  methods: {
    loadData(table, init=false) {
    	if (init) this.tableData = [];
			dataLoader.loadTableData(table, this.limit, (data, status) => {
				if (data) {
					this.tableData = [...this.tableData, ...data];
					this.status = status;
				} else {
					console.error('Не удалось загрузить данные');
				}
			});
    },
  },
  beforeDestroy() {
    dataLoader.cancel();
  },

};
</script>