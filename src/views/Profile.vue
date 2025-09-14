<template>
  <div>
    <Header />
    <v-container class="mb-8">
      <div
        class="profile-container d-flex flex-row justify-space-between mb-8 align-center"
      >
        <h1 class="white--text">Welcome, {{ user }}</h1>
        <p class="white--text ma-0">Total Watched: {{ watchedTotal }}</p>
      </div>
      <v-divider color="#561a7d"></v-divider>
      <div class="favorite-movies d-flex flex-row justify-space-between mt-8">
        <div v-if="likedMovies.length === 0" class="pa-4">
          <p class="white--text mb-10 text-center">
            You don't have any favorite movies yet.
            <br />
            <span class="grey--text caption text-center"
              >You can like a movie by clicking the heart icon on the movie
              detail page.</span
            >
          </p>
        </div>
        <div
          v-if="likedMovies.length > 0"
          class="favorite-movies d-flex flex-column"
        >
          <p class="white--text mb-10">Your Favorite Movies</p>
          <v-carousel
            height="400"
            show-arrows-on-hover
            cycle
            hide-delimiter-background
          >
            <v-carousel-item v-for="(movie, i) in likedMovies" :key="i">
              <v-sheet
                color="#1a0c33"
                height="100%"
                class="d-flex justify-center align-center"
              >
                <img
                  :src="movie.poster"
                  alt="Favorite Movie Poster"
                  style="
                    max-height: 100%;
                    border-radius: 10px;
                    border: 3px solid #561a7d;
                  "
                />
              </v-sheet>
            </v-carousel-item>
          </v-carousel>
        </div>
        <div v-if="watchlistMovies.length === 0" class="pa-4">
          <p class="white--text mb-10 text-center">
            You don't have any watchlist movies yet.
            <br />
            <span class="grey--text caption text-center"
              >You can add a movie to your watchlist by clicking the bookmark
              icon on the movie detail page.</span
            >
          </p>
        </div>
        <div
          v-if="watchlistMovies.length > 0"
          class="favorite-movies d-flex flex-column"
        >
          <p class="white--text mb-10">Your Watchlist Movies</p>
          <v-carousel
            height="400"
            show-arrows-on-hover
            cycle
            hide-delimiter-background
          >
            <v-carousel-item v-for="(movie, i) in watchlistMovies" :key="i">
              <v-sheet
                color="#1a0c33"
                height="100%"
                class="d-flex justify-center align-center"
              >
                <img
                  :src="movie.poster"
                  alt="Watchlist Movie Poster"
                  style="
                    max-height: 100%;
                    border-radius: 10px;
                    border: 3px solid #561a7d;
                  "
                />
              </v-sheet>
            </v-carousel-item>
          </v-carousel>
        </div>
        <div v-if="recentlyWatched.length === 0" class="pa-4">
          <p class="white--text mb-10 text-center">
            You don't have any recently watched movies yet.
            <br />
            <span class="grey--text caption text-center"
              >You can add a movie to your recently watched by clicking the
              watch icon on the movie detail page.</span
            >
          </p>
        </div>
        <div
          v-if="recentlyWatched.length > 0"
          class="favorite-movies d-flex flex-column"
        >
          <p class="white--text mb-10">Your Recently Watched</p>
          <v-carousel
            height="400"
            show-arrows-on-hover
            cycle
            hide-delimiter-background
          >
            <v-carousel-item v-for="(movie, i) in recentlyWatched" :key="i">
              <v-sheet
                color="#1a0c33"
                height="100%"
                class="d-flex justify-center align-center"
              >
                <img
                  :src="movie.poster"
                  alt="Recently Watched Movie Poster"
                  style="
                    max-height: 100%;
                    border-radius: 10px;
                    border: 3px solid #561a7d;
                  "
                />
              </v-sheet>
            </v-carousel-item>
          </v-carousel>
        </div>
      </div>
    </v-container>
    <Footer />
  </div>
</template>
<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
export default {
  name: "Profile",
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      user: null,
      watchedTotal: 0,
      likedMovies: [],
      watchlistMovies: [],
      recentlyWatched: [],
    };
  },
  mounted() {
    document.title = "Cinemajoo - Profile ";
    this.user = JSON.parse(localStorage.getItem("user"));
    const watched = JSON.parse(localStorage.getItem("watched")) || {};
    this.watchedTotal = watched[this.user]?.length || 0;
    const liked = JSON.parse(localStorage.getItem("liked")) || {};
    this.likedMovies = liked[this.user] || [];
    const watchlist = JSON.parse(localStorage.getItem("watchlist")) || {};
    this.watchlistMovies = watchlist[this.user] || [];
    const recently = JSON.parse(localStorage.getItem("recentlyWatched")) || {};
    this.recentlyWatched = recently[this.user] || [];
  },
};
</script>
<style scoped>
.profile-container p {
  font-size: 1.5rem;
  letter-spacing: 3px;
}

.profile-container h1 {
  letter-spacing: 6px;
}

.favorite-movies p {
  font-size: 1.25rem;
  letter-spacing: 3px;
  text-align: center;
}

.favorite-movie {
  width: 170px;
  height: 210px;
  border: 3px solid #561a7d;
  border-radius: 8px;
}
</style>
