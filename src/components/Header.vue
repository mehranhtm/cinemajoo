<template>
  <v-app-bar color="#2c1750" class="header">
    <div class="d-flex flex-row align-center">
      <div class="d-flex flex-row align-center logo-section">
        <img src="../assets/images/logo1.png" alt="logo" />
        <h1 class="white--text ml-3">Cinemajoo</h1>
      </div>
      <div class="d-flex flex-row align-center navigation-section">
        <p class="white--text mr-4">word1</p>
        <p class="white--text mr-4">word2</p>
        <p class="white--text mr-4">word3</p>
      </div>
    </div>
    <v-spacer></v-spacer>
    <v-text-field
      v-if="showSearch"
      v-model="searchQuery"
      placeholder="Search for a movie..."
      color="white"
      dark
      class="search-field"
      hide-details
      outlined
      @blur="hideSearch"
      ref="searchInput"
    ></v-text-field>
    <v-btn icon @click="toggleSearch" class="search-btn">
      <v-icon color="white">mdi-magnify</v-icon>
    </v-btn>
    <v-btn icon @click="handleLogout" class="logout-btn">
      <v-icon color="white">mdi-logout</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      showSearch: false,
      searchQuery: "",
    };
  },
  methods: {
    toggleSearch() {
      this.showSearch = !this.showSearch;
      if (this.showSearch) {
        this.$nextTick(() => {
          this.$refs.searchInput.focus();
        });
      }
    },
    hideSearch() {
      setTimeout(() => {
        this.showSearch = false;
      }, 200);
    },
    handleLogout() {
      localStorage.removeItem("user");
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.header {
  height: 85px !important;
}

.header img {
  width: 4%;
}

.logo-section {
  gap: 8px;
}

.navigation-section {
  gap: 16px;
  margin-left: 32px;
}

.navigation-section p {
  margin: 0;
  cursor: pointer;
  transition: color 0.2s ease;
}

.navigation-section p:hover {
  color: #ffd700 !important;
}

.search-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.logout-btn {
  color: white !important;
  width: 100%;
}
</style>
