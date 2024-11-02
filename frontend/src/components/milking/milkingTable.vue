<template>

	<div v-if="status > 0" class="table-container" style="min-width: 800px; max-width: 2000px;">
		<baseTable :data="itemsWithClasses" :columns="tableColumns" :status="status" :table="table" @child-mounted="cMounted = true"/><!--child1-->
	</div>
</template>

<script>
import baseTable from '../baseTable.vue';
import dataLoader from '@/utils/dataLoader';

export default {
	watch: {
		iMounted(n, o) {if(n && this.cMounted) this.$emit("child-mounted");},
		cMounted(n, o) {if(n && this.iMounted) this.$emit("child-mounted");},
	},
  components: {
    baseTable,
  },
  data() {
    return {
    	iMounted: false,
    	cMounted: false,
    	table: 'milking',
    	status: 0,
      tableData: [],
      limit: 500,
      offset: 0,
      tableColumns: [
        { key: 'id', label: 'ID', type: 'number' },
        { key: 'date', label: 'Дата дойки', type: 'date' },
        { key: 'fio', label: 'ФИО ответственного', type: 'string' },
        { key: 'cows', label: 'Коров', type: 'number' },
        { key: 'milk', label: 'Надоено, л', type: 'number' },
        { key: 'milk_e', label: 'в т.ч.Экстра', type: 'number' },
        { key: 'milk_h', label: 'в т.ч.Высший', type: 'number' },
        { key: 'milk_1', label: 'в т.ч.Первый', type: 'number' },
        { key: 'fat', label: 'Жирность,%', type: 'number' },
        { key: 'prot', label: 'Белок,%', type: 'number' },

      ],
    };
  },
	mounted() {
		dataLoader.loadTableData(this.table, this.limit, (data, status) => {
			if (data) {
				this.tableData = [...this.tableData, ...data];
				this.status = status;
			} else {
				console.error('Не удалось загрузить данные');
			}
		});
		this.iMounted = true;
  },
  computed: {
    itemsWithClasses() {
      return this.tableData.map(item => {
        const dictClass = {};

				switch (true) {
					case item.fat > 3.7:
						dictClass["fat"] = "success";
						break;
					case item.fat >= 3.3 && item.fat < 3.5:
						dictClass["fat"] = "warning";
						break;
					case item.fat < 3.3:
						dictClass["fat"] = "error";
				};

        return {
          ...item,
          dictClass: dictClass,
        };
      });
    }
  },

};
</script>