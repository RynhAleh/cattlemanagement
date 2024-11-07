<template>
  <div>
    <form @submit.prevent="submitForm">
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
import apiClient from '@/axios';

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
  mounted() {
		this.$emit("child-mounted");
  },

  methods: {
    async submitForm() {
      try {
        const response = await apiClient.post('/cattle', this.formData);
        this.$emit("update-data");
        this.$emit("close");
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