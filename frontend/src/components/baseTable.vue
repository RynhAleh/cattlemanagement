<template>
  <div>
    <button @click="getModalComponent">Добавить запись</button>
    <component :is="modalComponent" v-if="isModalPushed" @close="modalComponent = null" :table="table" />
  </div>
	<div class="filter-pagination">
		<div>
			<table>
				<tbody>
					<tr>
						<td>
							<select class="mg-5" v-model="selectedField" @change="filterData">
								<option value="all">(любое поле)</option>
								<option v-for="column in columns" :key="column.key" :value="column.key">
									{{ column.label }}
								</option>
							</select>
						</td>
						<td>
							<div v-if="currentFilterType === 'string'">
								<input class="txt-flt" type="text" v-model="filterQuery" @input="filterData" placeholder="Поиск..." />
							</div>
							<div v-if="currentFilterType === 'number'">
								<input class="num-flt" type="number" v-model="filterRange.min" @input="filterData" placeholder="С..." />
								-
								<input class="num-flt" type="number" v-model="filterRange.max" @input="filterData" placeholder="По..." />
							</div>
							<div v-if="currentFilterType === 'date'">
								<input class="dt-flt" type="date" v-model="filterDateRange.from" @input="filterData" />
								-
								<input class="dt-flt" type="date" v-model="filterDateRange.to" @input="filterData" />
							</div>
						</td>
						<td>
							<select v-model="logicOperator">
								<option value="x"> </option>
								<option value="AND">И</option>
								<option value="OR">ИЛИ</option>
							</select>
						</td>
						<td class="mg-5" style="color: gray;">{{ status > 1 ? 'Записей: ' + filteredData.length + '.' : '' }}</td>
					</tr>
					<tr v-if="isSecondFilterActive">
						<td>
							<select class="mg-5" v-model="selectedSecondField" @change="filterData">
								<option value="all">(любое поле)</option>
								<option v-for="column in columns" :key="column.key" :value="column.key">
									{{ column.label }}
								</option>
							</select>
						</td>
						<td>
							<div v-if="currentSecondFilterType === 'string'">
								<input class="txt-flt" type="text" v-model="secondFilterQuery" @input="filterData" placeholder="Поиск..." />
							</div>
							<div v-if="currentSecondFilterType === 'number'">
								<input class="num-flt" type="number" v-model="secondFilterRange.min" @input="filterData" placeholder="С..." />
								-
								<input class="num-flt" type="number" v-model="secondFilterRange.max" @input="filterData" placeholder="По..." />
							</div>
							<div v-if="currentSecondFilterType === 'date'">
								<input class="dt-flt" type="date" v-model="secondFilterDateRange.from" @input="filterData" />
								-
								<input class="dt-flt" type="date" v-model="secondFilterDateRange.to" @input="filterData" />
							</div>
						</td>
						<td></td>
						<td></td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
	<table class="custom-table">
		<thead>
			<tr>
				<th v-for="column in columns" :key="column.key" @click="sortData(column.key)">
					{{ column.label }}
					<span v-if="sortKey === column.key">
						{{ sortOrder === 'asc' ? '▲' : sortOrder === 'desc' ? '▼' : '' }}
					</span>
				</th>
			</tr>
		</thead>
		<tbody>
      <tr v-for="row in paginatedData" :key="row.id" v-bind="row.dictClass['_'] ? { class: row.dictClass['_'] } : {}">
        <td v-for="column in columns" :key="column.key" v-bind="row.dictClass[column.key] ? { class: row.dictClass[column.key] } : {}">
          {{ row[column.key] }}
        </td>
      </tr>
		</tbody>
	</table>
	<div class="info-pagination">
		<div>
			<button class="btn-flt" @click="firstPage" :disabled="currentPage === 1"><<</button>
			<button class="btn-flt" @click="prevPage" :disabled="currentPage === 1"><</button>
			<span class="page-from-pages">{{ currentPage }} из {{ totalPages }}</span>
			<button class="btn-flt" @click="nextPage" :disabled="currentPage === totalPages">></button>
			<button class="btn-flt" @click="lastPage" :disabled="currentPage === totalPages">>></button>
			<label class="mg-5" for="rowsPerPage">Записей на стр.:</label>
			<select v-model="rowsPerPage" @change="normalizePage">
				<option value=20>20</option>
				<option value=50>50</option>
				<option value=100>100</option>
				<option value=1000>1000</option>
				<option value=99999999>(все)</option>
			</select>
		</div>
	</div>
</template>

<script>
import { markRaw } from 'vue';
export default {
//  components: {
//    modalComponent,
//  },
  props: {
  	table: String,
    data: Array,
    columns: Array,
		status: Number,
  },
  data() {
    return {
    	modalComponent: null,
    	isModalPushed: false,
      sortKey: '',
      sortOrder: '',
      filterQuery: '',             // Значение первого фильтра
      selectedField: 'all',        // Поле для первого фильтра
      secondFilterQuery: '',       // Значение второго фильтра
      selectedSecondField: 'all',  // Поле для второго фильтра
      currentPage: 1,
      rowsPerPage: 20,
      filterRange: { min: null, max: null },
      secondFilterRange: { min: null, max: null }, // Диапазон для второго фильтра
      filterDateRange: { from: null, to: null },
      secondFilterDateRange: { from: null, to: null }, // Диапазон дат для второго фильтра
      logicOperator: 'x',          // Выпадающий список: x, И, ИЛИ
      filteredData: [],
      isSecondFilterActive: false
    };
  },
  watch: {
    data: {
      handler(newData) {
        this.filteredData = newData.slice();
        this.filterData(); // Фильтрация данных при изменении входных данных
      },
      immediate: true
    },
    logicOperator(newValue) {
      this.isSecondFilterActive = newValue !== 'x'; // Активен ли второй фильтр
      if (!this.isSecondFilterActive) {
        this.secondFilterQuery = ''; // Сброс второго фильтра
      }
      this.filterData();
    }
  },
  computed: {
    totalPages() {
      return Math.ceil(this.filteredData.length / this.rowsPerPage);
    },
    paginatedData() {
      const start = (this.currentPage - 1) * this.rowsPerPage;
      return this.filteredData.slice(start, Number(start) + Number(this.rowsPerPage));
    },
    currentFilterType() {
      if (this.selectedField === 'all') return 'string';
      const column = this.columns.find(col => col.key === this.selectedField);
      return column ? column.type : 'string';
    },
    currentSecondFilterType() {
      if (this.selectedSecondField === 'all') return 'string';
      const column = this.columns.find(col => col.key === this.selectedSecondField);
      return column ? column.type : 'string';
    }
  },
  methods: {
    // Фильтрация данных
    filterData() {

			let filterConditions = []; // массив для накопления условий фильтрации

			// Генерация условий фильтрации
			if (this.selectedField === 'all') {
				filterConditions.push(item =>
					Object.values(item).some(value =>
						String(value).toLowerCase().includes(this.filterQuery.toLowerCase())
					)
				);
			} else {
				const columnType = this.currentFilterType;
				if (columnType === 'string') {
					filterConditions.push(item =>
						String(item[this.selectedField]).toLowerCase().includes(this.filterQuery.toLowerCase())
					);
				} else if (columnType === 'number') {
					const min = this.filterRange.min || Number.MIN_SAFE_INTEGER;
					const max = this.filterRange.max || Number.MAX_SAFE_INTEGER;
					filterConditions.push(item =>
						item[this.selectedField] >= min && item[this.selectedField] <= max
					);
				} else if (columnType === 'date') {
					const fromDate = new Date(this.filterDateRange.from || '1900-01-01');
					const toDate = new Date(this.filterDateRange.to || '9999-12-31');
					filterConditions.push(item => {
						const itemDate = new Date(item[this.selectedField]);
						return itemDate >= fromDate && itemDate <= toDate;
					});
				}
			}
      if (this.isSecondFilterActive) {
//				console.log(this.isFilled(this.secondFilterQuery), this.isFilled(this.secondFilterDateRange.min), this.isFilled(this.secondFilterDateRange.max), this.isFilled(this.secondFilterDateRange.from), this.isFilled(this.secondFilterDateRange.to))
//				console.log(this.secondFilterQuery, this.secondFilterDateRange.min, this.secondFilterDateRange.max, this.secondFilterDateRange.from, this.secondFilterDateRange.to)
				if (this.selectedSecondField === 'all') {
					if (this.isFilled(this.secondFilterQuery)) {
						filterConditions.push(item =>
							Object.values(item).some(value =>
								String(value).toLowerCase().includes(this.secondFilterQuery.toLowerCase())
							)
						);
					}
				} else {
					const columnType = this.currentSecondFilterType;
					if (columnType === 'string' && this.isFilled(this.secondFilterQuery)) {
						filterConditions.push(item =>
							String(item[this.selectedSecondField]).toLowerCase().includes(this.secondFilterQuery.toLowerCase())
						);
					} else if (columnType === 'number') {
						const min = this.secondFilterRange.min || Number.MIN_SAFE_INTEGER;
						const max = this.secondFilterRange.max || Number.MAX_SAFE_INTEGER;
						if (this.isFilled(this.secondFilterRange.min) || this.isFilled(this.secondFilterRange.max)) {
							filterConditions.push(item =>
								item[this.selectedSecondField] >= min && item[this.selectedSecondField] <= max
							);
						}
					} else if (columnType === 'date') {
						const fromDate = new Date(this.secondFilterDateRange.from || '1900-01-01');
						const toDate = new Date(this.secondFilterDateRange.to || '9999-12-31');
						if (this.isFilled(this.secondFilterDateRange.from) || this.isFilled(this.secondFilterDateRange.to)) {
							filterConditions.push(item => {
								const itemDate = new Date(item[this.selectedSecondField]);
								return itemDate >= fromDate && itemDate <= toDate;
							});
						}
					}
				}
//				console.log(filterConditions.length, filterConditions[0], filterConditions[1])
				this.filteredData = this.data.filter(item => {
					if (this.logicOperator === 'AND') {
						// Проверка, чтобы все условия вернули true (логика AND)
						return filterConditions.every(condition => condition(item));
					} else if (this.logicOperator === 'OR') {
						// Проверка, чтобы хотя бы одно условие вернуло true (логика OR)
						return filterConditions.some(condition => condition(item));
					}
				});
			} else {
				// Если второй фильтр не сработал
				this.filteredData = this.data.filter(item =>
					filterConditions.every(condition => condition(item))
				);
			}
      this.currentPage = 1; // Сброс на первую страницу после фильтрации

      // Применяем сортировку после фильтрации
      if (this.sortKey && this.sortOrder) {
        this.sortData(this.sortKey, true);
      }
    },
    // Сортировка данных
    sortData(key, preserveOrder = false) {
      if (!preserveOrder) {
        if (this.sortKey === key) {
          if (this.sortOrder === '') {
            this.sortOrder = 'asc'; // Первое нажатие - по возрастанию
          } else if (this.sortOrder === 'asc') {
            this.sortOrder = 'desc'; // Второе нажатие - по убыванию
          } else {
            this.sortKey = ''; // Сброс ключа сортировки
            this.sortOrder = ''; // Сброс состояния сортировки
            // В третьем состоянии сброса сортировки применяем только фильтрацию
            this.filteredData = this.data.slice(); // Возвращаем к исходным данным
            this.filterData(); // Применяем фильтр снова
            return;
          }
        } else {
          this.sortKey = key;
          this.sortOrder = 'asc';
        }
      }

      this.filteredData.sort((a, b) => {
        const modifier = this.sortOrder === 'asc' ? 1 : -1;
        if (a[key] < b[key]) return -1 * modifier;
        if (a[key] > b[key]) return 1 * modifier;
        return 0;
      });
    },

    firstPage() {
      this.currentPage = 1;
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    lastPage() {
      this.currentPage = this.totalPages;
    },
    normalizePage() {
      if (this.currentPage > this.totalPages) {
        this.currentPage = this.totalPages;
      }
    },
    isFilled(value) {
      return value !== '' && value !== undefined && value !== null;
    },
		getModalComponent() {
			import('./modalForm.vue').then((module) => {
				this.modalComponent = markRaw(module.default);
				this.isModalPushed = true;
			});
		},
  }
};
</script>
