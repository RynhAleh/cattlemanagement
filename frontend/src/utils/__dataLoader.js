import apiClient from '@/axios';

export default {
  async loadTableData(table, limit, onDataLoaded) {
  	let isComplete = false;
    try {
      // Загружаем первую порцию данных с указанным лимитом
      const firstResponse = await apiClient.get(`/${table}?limit=${limit}&offset=0`);
      const firstData = firstResponse.data;

      // Передаем первую порцию данных через коллбэк

      onDataLoaded(firstData, firstData.length < limit ? 2 : 1);

      // Если количество данных равно лимиту, загружаем оставшиеся данные
      if (firstData.length === limit) {
        const remainingResponse = await apiClient.get(`/${table}?offset=${limit}`);
        const remainingData = remainingResponse.data;

        // Передаем оставшиеся данные через коллбэк
        onDataLoaded(remainingData, 2);
      }
    } catch (error) {
      console.error('Ошибка при загрузке данных:', error);
      onDataLoaded(null); // Сообщаем компоненту об ошибке
    }
  }
};