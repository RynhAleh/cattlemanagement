<template>
  <div>
    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="id">ID</label>
        <input type="number" id="id" v-model="formData.id" class="form-control" />
      </div>

      <div class="form-group">
        <label for="name">Имя или инд.номер</label>
        <input type="text" id="name" v-model="formData.name" class="form-control" />
      </div>

      <div class="form-group">
        <label for="color">Цвет/окрас, лет</label>
        <input type="text" id="color" v-model="formData.color" class="form-control" />
      </div>

      <div class="form-group">
        <label for="breed">Порода</label>
        <input type="text" id="breed" v-model="formData.breed" class="form-control" />
      </div>

      <div class="form-group">
        <label for="birthdate">Дата рождения</label>
        <input type="date" id="birthdate" v-model="formData.birthdate" class="form-control" />
      </div>

      <button type="submit" class="btn btn-primary">Отправить</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      formData: {
        id: null,
        name: '',
        color: '',
        breed: '',
        birthdate: '',
      },
    };
  },
  methods: {
    async submitForm() {
      try {
        const response = await axios.post('/api/cattle', this.formData);
        alert('Данные успешно отправлены!');
        console.log(response.data);
      } catch (error) {
        console.error('Ошибка отправки данных:', error);
        alert('Произошла ошибка при отправке данных.');
      }
    },
  },
};
</script>

<style scoped>
.form-group {
  margin-bottom: 1rem;
}

label {
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.5rem;
  margin-top: 0.5rem;
}
</style>