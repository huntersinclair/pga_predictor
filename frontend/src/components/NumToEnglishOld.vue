<template>
  <div class="container mt-5">
    <h1>Number to English</h1>
    <div class="mb-3">
      <input v-model="number" class="form-control" placeholder="Enter a number" />
    </div>
    <button @click="handleRequest('GET')" class="btn btn-primary me-2">Convert (GET)</button>
    <button @click="handleRequest('POST')" class="btn btn-secondary">Convert (POST with Delay)</button>
    
    <div v-if="loading" class="d-flex justify-content-center mt-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="numInEnglish" class="alert alert-success mt-3">Result: {{ numInEnglish }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      number: '',
      numInEnglish: '',
      loading: false,
      error: ''
    };
  },
  methods: {
    async handleRequest(method) {
      if (!this.number.trim()) {
        this.error = 'Please enter a number.';
        return;
      }

      this.loading = true;
      this.error = '';
      this.numInEnglish = '';

      if (method === 'GET') {
        await this.getNumberInEnglish();
      } else if (method === 'POST') {
        await this.postNumberInEnglish();
      }

      this.loading = false;
    },
    async getNumberInEnglish() {
      try {
        const response = await fetch(`${process.env.VUE_APP_API_URL}?number=${this.number}`);
        const data = await response.json();
        if (data.status === 'ok') {
          this.numInEnglish = data.num_in_english;
        } else {
          this.error = data.message || 'Failed to convert number.';
        }
      } catch (err) {
        this.error = 'Error occurred while converting number.';
      }
    },
    async postNumberInEnglish() {
      try {
        // 5-second delay
        await new Promise(resolve => setTimeout(resolve, 5000));

        const response = await fetch(`${process.env.VUE_APP_API_URL}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ number: this.number })
        });
        const data = await response.json();
        if (data.status === 'ok') {
          this.numInEnglish = data.num_in_english;
        } else {
          this.error = data.message || 'Failed to convert number.';
        }
      } catch (err) {
        this.error = 'Error occurred while converting number.';
      }
    }
  }
};
</script>

<style>
.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>
