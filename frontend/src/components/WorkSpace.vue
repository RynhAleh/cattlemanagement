<template>
  <div>
    <h1>Список животных</h1>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Имя</th>
            <th>Окрас</th>
            <th>Дата рождения</th>
            <th>Вес при рождении</th>          
            <!-- Добавьте дополнительные заголовки для всех полей -->
          </tr>
        </thead>
        <tbody>
          <tr v-for="animal in cattle" :key="animal.id">
            <td>{{ animal.id }}</td>
            <td>{{ animal.name }}</td>
            <td>{{ animal.color }}</td>
            <td>{{ animal.breed }}</td>
            <td>{{ animal.birthdate }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <h2>Добавить животное</h2>
    <form @submit.prevent="addCattle">
      <label for="f01">Кличка:</label>
      <input id="f01" type="text" v-model="newCattle.name" required />
      
      <label for="f02">Окрас:</label>
      <input id="f02" type="text" v-model="newCattle.color" required />
      
      <label for="f03">Порода:</label>
      <input id="f03" type="text" v-model="newCattle.breed" required />

      <label for="f04">Дата рождения:</label>
      <input id="f04" type="date" v-model="newCattle.birthdate" />

      <button type="submit">Добавить</button>
    </form>

  </div>
</template>

<script>
import apiClient from '@/axios';
export default {
  data() {
    return {
      cattle: [], // Список животных
      newCattle: {
        name: '',
        color: '',
        breed: '',
        birthdate: ''
      }
    };
  },
  created() {
    this.fetchCattle(); // Запрос данных при создании компонента
  },
  methods: {
    async fetchCattle() {
      try {
        const response = await apiClient.get('/cattle'); // Относительный путь
        this.cattle = response.data; // Запись данных в cattle
      } catch (error) {
        console.error('Ошибка при получении данных:', error);
      }
    },
    async addCattle() {
      try {
        const response = await apiClient.post('/cattle', this.newCattle); // Относительный путь и данные животного
        this.cattle.push(response.data); // Добавляем нового животного в список
        // Очищаем поля формы
        this.newCattle.name = '';
        this.newCattle.color = '';
        this.newCattle.breed = '';
        this.newCattle.birthdate = '';
      } catch (error) {
        console.error('Ошибка при добавлении животного:', error);
      }
    },
  },
};
</script>

<style scoped>
.table-container {
  width: calc(100% - 0px); /* Замените 250px на фактическую ширину боковой панели */
  height: calc(100vh - 350px); /* Высота страницы минус форма ввода (например, 150px) */
  overflow-y: auto;
  border: 1px solid #ddd;
}

table {
  width: 100%;
  border-collapse: collapse;
}

table th {
  padding: 10px;
  border: 1px solid #ccc;
  background-color: #e2ffe2; /* Бледно-зелёный цвет для шапки таблицы */
  color: #000; /* Цвет текста в шапке */
}

table td {
  padding: 10px;
  border: 1px solid #ccc;
}
</style>