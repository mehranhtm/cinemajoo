<template>
  <v-app-bar color="#2c1750" class="header">
    <div class="d-flex flex-row align-center">
      <div class="d-flex flex-row align-center logo-section">
        <img src="../assets/images/logo1.png" alt="logo" />
        <h1
          class="white--text ml-3"
          v-show="!($vuetify.breakpoint.smAndDown && showSearch)"
        >
          Cinemajoo
        </h1>
      </div>
      <div
        class="d-flex flex-row align-center navigation-section"
        v-show="$vuetify.breakpoint.mdAndUp"
      >
        <p
          class="white--text text-center caption mr-4"
          @click="$router.push('/toprate')"
        >
          Top 20 Movies
        </p>
      </div>
    </div>
    <v-spacer></v-spacer>
    <div class="search-container">
      <v-text-field
        v-show="showSearch"
        v-model="searchQuery"
        placeholder="Search for a movie..."
        color="white"
        dark
        class="search-field"
        hide-details
        outlined
        @blur="hideSearch"
        ref="searchInput"
        @input="searchMovies"
        @focus="handleShowDropdown"
      >
      </v-text-field>
      <v-card
        v-if="showDropdown && searchQuery !== ''"
        class="search-dropdown"
        elevation="8"
      >
        <v-list v-if="searchResults.length > 0">
          <v-list-item
            v-for="movie in searchResults"
            :key="movie.id"
            @click="goToMovie(movie)"
            class="search-result-item"
          >
            <v-list-item-avatar>
              <v-img
                :src="
                  movie.poster_url
                    ? movie.poster_url
                    : 'https://via.placeholder.com/92x138?text=No+Image'
                "
              />
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>{{ movie.title }}</v-list-item-title>
              <v-list-item-subtitle>
                {{ movie.release_date }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-list v-else-if="isLoading">
          <v-list-item>
            <v-list-item-content class="d-flex align-center">
              <v-progress-circular
                indeterminate
                size="22"
                color="white"
                class="mr-2"
              />
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-list v-else-if="searchQuery && searchResults.length === 0">
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="white--text"
                >No results found
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>
    </div>
    <v-tooltip bottom>
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          icon
          @click="toggleSearch"
          class="search-btn"
          v-bind="attrs"
          v-on="on"
          v-show="!($vuetify.breakpoint.smAndDown && showSearch)"
        >
          <v-icon color="white">mdi-magnify</v-icon>
        </v-btn>
      </template>
      <span>Search Movies</span>
    </v-tooltip>
    <v-menu
      v-if="$vuetify.breakpoint.smAndDown"
      v-model="mobileMenu"
      offset-y
      transition="fade-transition"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon class="menu-btn" v-bind="attrs" v-on="on">
          <v-icon color="white">mdi-menu</v-icon>
        </v-btn>
      </template>
      <v-list class="mobile-menu-list">
        <v-list-item
          @click="
            $router.push('/toprate');
            mobileMenu = false;
          "
        >
          <v-list-item-title>Top 20 Movies</v-list-item-title>
        </v-list-item>
        <v-list-item
          @click="
            $router.push('/watchlist');
            mobileMenu = false;
          "
        >
          <v-list-item-title>Watchlist</v-list-item-title>
        </v-list-item>
        <v-list-item
          @click="
            $router.push('/profile');
            mobileMenu = false;
          "
        >
          <v-list-item-title>Profile</v-list-item-title>
        </v-list-item>
        <v-list-item
          @click="
            handleLogout();
            mobileMenu = false;
          "
        >
          <v-list-item-title>Logout</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <div
      v-show="$vuetify.breakpoint.mdAndUp"
      class="desktop-actions d-flex flex-row align-center"
    >
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            @click="$router.push('/watchlist')"
            v-bind="attrs"
            v-on="on"
            class="watchlist-btn"
          >
            <img
              style="width: inherit; filter: brightness(0) invert(1)"
              src="../assets/images/watchlist.svg"
              alt="watchlist"
            />
          </v-btn>
        </template>
        <span>Your Watchlist</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            @click="$router.push('/profile')"
            class="profile-btn"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon color="white">mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <span>Profile</span>
      </v-tooltip>
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            icon
            @click="handleLogout"
            class="logout-btn"
            v-bind="attrs"
            v-on="on"
          >
            <v-icon color="white">mdi-logout</v-icon>
          </v-btn>
        </template>
        <span>Logout</span>
      </v-tooltip>
    </div>
  </v-app-bar>
</template>

<script>
export default {
  name: "Header",
  data() {
    return {
      showSearch: false,
      searchQuery: "",
      searchResults: [],
      showDropdown: false,
      searchTimeout: null,
      isLoading: false,
      mobileMenu: false,
    };
  },
  methods: {
    toggleSearch() {
      this.showSearch = !this.showSearch;
      if (this.showSearch) {
        this.$nextTick(() => {
          this.$refs.searchInput.focus();
        });
      } else {
        this.showDropdown = false;
        this.searchQuery = "";
        this.searchResults = [];
      }
    },
    hideSearch() {
      setTimeout(() => {
        this.showSearch = false;
        this.showDropdown = false;
        this.searchQuery = "";
        this.searchResults = [];
      }, 200);
    },
    handleShowDropdown() {
      if (this.searchQuery.trim()) {
        this.showDropdown = true;
      }
    },
    handleLogout() {
      localStorage.removeItem("user");
      this.$router.push("/");
    },
    async searchMovies() {
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }
      this.isLoading = true;
      if (!this.searchQuery.trim()) {
        this.searchResults = [];
        this.showDropdown = false;
        this.isLoading = false;
        return;
      }
      this.showDropdown = true;
      this.searchTimeout = setTimeout(async () => {
        try {
          const response = await fetch(
            `http://localhost:8000/api/movies/search?q=${encodeURIComponent(
              this.searchQuery
            )}`
          );
          const data = await response.json();
          this.searchResults = data;
        } catch (err) {
          console.error("Error fetching search results:", err);
          this.searchResults = [];
        } finally {
          this.isLoading = false;
        }
      }, 5);
    },
    goToMovie(movie) {
      this.$router.push(`/movie/${movie.id}`);
      this.showDropdown = false;
      this.searchQuery = "";
      this.searchResults = [];
      this.showSearch = false;
    },
  },
};
</script>

<style scoped>
.header {
  height: 85px !important;
  position: relative;
  z-index: 4000;
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

.menu-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.logout-btn {
  color: white !important;
  width: 100%;
}

.search-container {
  position: relative;
  margin-right: 8px;
}

.search-field {
  min-width: 100px;
}

.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  z-index: 5000;
  max-height: 400px;
  overflow-y: auto;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: white !important;
}

.search-dropdown.v-card {
  background-color: #1a0c33 !important;
}

.search-dropdown .v-list {
  background-color: #1a0c33 !important;
}

.search-result-item {
  cursor: pointer;
  transition: background-color 0.2s ease;
  background-color: transparent !important;
}

.search-result-item:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.search-result-item .v-list-item__title {
  color: white !important;
}

.search-result-item .v-list-item__subtitle {
  color: rgba(255, 255, 255, 0.7) !important;
}

.search-dropdown::-webkit-scrollbar {
  width: 8px;
}

.search-dropdown::-webkit-scrollbar-track {
  background: #1a1a1a;
  border-radius: 4px;
}

.search-dropdown::-webkit-scrollbar-thumb {
  background: #2c1750;
  border-radius: 4px;
  border: 1px solid #2c1750;
}

.search-dropdown::-webkit-scrollbar-thumb:hover {
  background: #2c1750;
}

.search-dropdown {
  scrollbar-width: thin;
  scrollbar-color: #2c1750 #1a1a1a;
}

.profile-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.watchlist-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
.watchlist-btn >>> .v-btn__content {
  width: 30px !important;
  height: 30px !important;
}

.mobile-menu-list {
  background-color: #1a0c33 !important;
  color: white !important;
}
.mobile-menu-list .v-list-item__title {
  color: white !important;
}
@media (max-width: 768px) {
  .header img {
    display: none;
  }
  .header h1 {
    font-size: 20px !important;
    margin-left: 0 !important;
  }
  .navigation-section,
  .desktop-actions {
    display: none !important;
  }
}
</style>
