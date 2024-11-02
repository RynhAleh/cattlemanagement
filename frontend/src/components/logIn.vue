<template>
  <div class="wrapper">
  <div class="login-container">
    <h2>Вход в систему</h2>
    <form @submit.prevent="handleLogin">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" v-model="username" id="username" required autocomplete="username" />
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" v-model="password" id="password" required autocomplete="current-password" />
      </div>
      <button class="button" type="submit">Войти</button>
    </form>
    <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
  </div>
  </div>
</template>

<script>
import apiClient from '@/axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      users: [],
      errorMessage: '',
    };
  },
  methods: {
		async handleLogin() {
			try {
				const response = await apiClient.post('/login', new URLSearchParams({
					username: this.username,
					password: this.password,
				}), {
					headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
				});
				localStorage.setItem('token', response.data.access_token); // Сохраните токен
				localStorage.setItem('isAuthenticated', true); // Установите состояние аутентификации
				this.$router.push('/app');
			} catch (error) {
				console.error('Вход не осуществлен:', error.response.data); // Отладочная информация
				this.errorMessage = 'Неверное имя пользователя или пароль'; // Сообщение об ошибке
			}
		},
  },
};
</script>

<style scoped>
.wrapper {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-container {
  width: 35vw;
  min-width: 200px;
  max-width: 350px;
  margin: -15vh 0 0 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: var(--primary-color);
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  font-size: 16px;
}

input[type="text"]:focus,
input[type="password"]:focus {
  border-color: #007BFF;
  outline: none;
}

.button {
  width: 100%;
}


</style>