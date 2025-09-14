<template>
  <div>
    <Header />
    <v-container>
      <h1 class="white--text mb-6">Watch List</h1>
      <v-row dense>
        <v-col
          v-for="movie in watchlistMovies"
          :key="movie.id"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card class="movie-card" @click="goToMovieDetail(movie.id)">
            <v-img
              :src="movie.poster"
              aspect-ratio="0.67"
              class="poster"
              :alt="`Poster of movie ID ${movie.id}`"
            ></v-img>
          </v-card>
        </v-col>
      </v-row>

      <p v-if="!watchlistMovies.length" class="grey--text text-center mt-6">
        Your watch list is empty.
      </p>
    </v-container>
    <Footer />
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "WatchList",
  components: { Header, Footer },
  data() {
    return {
      user: null,
      watchlistMovies: [],
    };
  },
  mounted() {
    document.title = "Cinemajoo - Watch List";
    this.user = JSON.parse(localStorage.getItem("user"));
    if (!this.user) return;
    const watchlist = JSON.parse(localStorage.getItem("watchlist")) || {};
    this.watchlistMovies = watchlist[this.user] || [];
    console.log(this.watchlistMovies);
  },
  methods: {
    goToMovieDetail(movieId) {
      this.$router.push(`/movie/${movieId}`);
    },
  },
};
</script>

<style scoped>
.movie-card {
  background-color: #1a0c33;
  border: 3px solid #561a7d;
  border-radius: 8px;
}
</style>
