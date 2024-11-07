import apiClient from '@/axios';

const dataLoader = {
  abortController: null,

  async loadTableData(table, limit, onDataLoaded) {
    this.abortController?.abort();
    this.abortController = new AbortController();
    const signal = this.abortController.signal;

    try {
      const firstResponse = await apiClient.get(`/${table}?limit=${limit}&offset=0`, { signal });
      onDataLoaded(firstResponse.data, firstResponse.data.length < limit ? 2 : 1);

      if (firstResponse.data.length === limit) {
        const remainingResponse = await apiClient.get(`/${table}?offset=${limit}`, { signal });
        onDataLoaded(remainingResponse.data, 2);
      }
    } catch (error) {
      if (error.name !== 'AbortError') {
        console.error('Ошибка при загрузке данных:', error);
        onDataLoaded(null);
      }
    } finally {
      this.abortController = null;
    }
  },

  cancel() {
    this.abortController?.abort();
    this.abortController = null;
  },
};

export default dataLoader;