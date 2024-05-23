<template>
  <div class="container mt-5">
    <h1>Get PGA Tournament Player Stats</h1>
    <div class="mb-3">
      <input v-model="number" class="form-control" placeholder="Enter the pga tournament id (starts with R)" />
    </div>
    <div class="mb-3">
      <input v-model="tournament_url" class="form-control" placeholder="Enter the url to the pga tournament page (including https://)" />
    </div>
    <div class="mb-3">
      <select v-model="file_type" class="form-control" placeholder="What type of file format (JSON or CSV)">
        <option value="csv" selected>CSV</option>
        <option value="json">JSON</option>
      </select>
    </div>
    <!-- button @click="handleRequest('GET')" class="btn btn-primary me-2">Convert (GET)</button -->
    <button @click="handleRequest('POST')" class="btn btn-secondary">RUN</button>
    
    <div v-if="loading" class="d-flex justify-content-center mt-3">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">Result: {{ success }}</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      number: '',
      success: '',
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
      if (!this.tournament_url.trim()) {
        this.error = 'Please enter a url to the tournament page on pga website.';
        return;
      }
      if (!this.file_type) {
        this.error = 'Please select a download file type.';
        return;
      }

      this.loading = true;
      this.error = '';
      this.success = '';

      if (method === 'GET') {
        await this.getNumberInEnglish();
      } else if (method === 'POST') {
        await this.postNumberInEnglish();
      }

      this.loading = false;
    },
    async getNumberInEnglish() {
      try {
        const response = await fetch(`${process.env.VUE_APP_API_PGA_URL}?number=${this.number}&tournament_url=${this.tournament_url}&file_type=${this.file_type}`);
        const data = await response.json();
        if (data.status === 'ok') {
          this.success = data.success;
        } else {
          this.error = data.message || 'Failed to get tournament stats.';
        }
      } catch (err) {
        this.error = 'Error occurred while getting tournament stats.';
      }
    },
    async postNumberInEnglish() {
      try {
        // 5-second delay
        // await new Promise(resolve => setTimeout(resolve, 5000));

        const response = await fetch(`${process.env.VUE_APP_API_PGA_URL}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ number: this.number, tournament_url: this.tournament_url, file_type: this.file_type})
        });
        const blob = await response.blob();    
        const newBlob = new Blob([blob]);    
        if (window.navigator && window.navigator.msSaveOrOpenBlob) {
          window.navigator.msSaveOrOpenBlob(newBlob);    
        } else {      
          // For other browsers: create a link pointing to the ObjectURL containing the blob.      
          const objUrl = window.URL.createObjectURL(newBlob);      
          const link = document.createElement("a");      
          link.href = objUrl;      
          link.download = "pga_tournament_stats_"+this.number+"."+this.file_type;      
          link.click();      
          // For Firefox it is necessary to delay revoking the ObjectURL.      
          setTimeout(() => {        
            window.URL.revokeObjectURL(objUrl);      
          }, 250);
          this.success = "File successfully downloaded."
        }  

        // const data = await response.json();
        // if (data.status === 'ok') {
        //   this.success = data.success;
        // } else {
        //   this.error = data.message || 'Failed to get tournament stats.';
        // }
      } catch (err) {
        this.error = 'Error occurred while getting tournament stats.';
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
