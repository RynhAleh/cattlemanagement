import apiClient from '@/axios';

const dataLoader = {
  abortController: null,
  currentRequestId: 0, // уникальный ID для каждого запроса

  async loadTableData(table, limit, onDataLoaded) {
    if (this.abortController) {
      this.abortController.abort();
    }

    this.abortController = new AbortController();
    const signal = this.abortController.signal;
    const requestId = ++this.currentRequestId; // новый ID для каждого запроса

    try {
      const firstResponse = await apiClient.get(`/${table}?limit=${limit}&offset=0`, { signal });
      if (requestId === this.currentRequestId) { // проверка актуальности запроса
        onDataLoaded(firstResponse.data, firstResponse.data.length < limit ? 2 : 1);
      }

      if (firstResponse.data.length === limit) {
        const remainingResponse = await apiClient.get(`/${table}?offset=${limit}`, { signal });
        if (requestId === this.currentRequestId) {
          onDataLoaded(remainingResponse.data, 2);
        }
      }
    } catch (error) {
      if (error.name !== 'AbortError' && requestId === this.currentRequestId) {
        console.error('Ошибка при загрузке данных:', error);
        onDataLoaded(null);
      }
    }
  },

  cancel() {
    this.abortController?.abort();
  },
};

export default dataLoader;