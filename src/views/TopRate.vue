<template>
  <div>
    <Header />
    <v-container>
      <h1 class="white--text mb-6">Top 20 Movies</h1>
      <v-divider color="#561a7d" class="mb-6"></v-divider>
      <div
        v-if="isLoading"
        class="d-flex justify-center align-center"
        style="min-height: 60vh"
      >
        <v-progress-circular
          color="purple"
          :size="64"
          :width="6"
          indeterminate
        ></v-progress-circular>
      </div>
      <v-row v-else>
        <v-col
          v-for="movie in top20Movies"
          :key="movie?.id || Math.random()"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          xl="2"
        >
          <v-card
            v-if="movie"
            class="movie-card"
            elevation="8"
            hover
            @click="goToMovieDetail(movie.id)"
          >
            <v-img
              :src="
                movie.poster_url ||
                'https://via.placeholder.com/300x450?text=No+Image'
              "
              :alt="movie.title || 'Movie'"
              height="400"
              class="movie-poster"
            >
              <template v-slot:placeholder>
                <v-row class="fill-height ma-0" align="center" justify="center">
                  <v-progress-circular
                    indeterminate
                    color="grey lighten-5"
                  ></v-progress-circular>
                </v-row>
              </template>
            </v-img>

            <v-card-text class="pa-3">
              <h3
                class="movie-title text-h6 mb-2 white--text"
                style="font-weight: bold"
              >
                {{ movie.title || "Unknown Title" }}
              </h3>

              <div class="d-flex align-center justify-space-between">
                <div class="d-flex align-center">
                  <v-icon color="amber" class="mr-1">mdi-star</v-icon>
                  <span
                    class="vote-average font-weight-bold white--text"
                  >
                    {{
                      movie.vote_average ? movie.vote_average.toFixed(1) : "N/A"
                    }}
                  </span>
                </div>

                <div class="release-year white--text" style="font-size: 0.9em">
                  {{
                    movie.release_date
                      ? new Date(movie.release_date).getFullYear()
                      : "N/A"
                  }}
                </div>
              </div>

              <div
                v-if="movie.summary_en"
                class="movie-summary mt-2 white--text"
                style="font-size: 0.85em; line-height: 1.3"
              >
                {{
                  movie.summary_en.length > 100
                    ? movie.summary_en.substring(0, 100) + "..."
                    : movie.summary_en
                }}
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
    <Footer />
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";

export default {
  name: "TopRate",
  components: {
    Header,
    Footer,
  },
  data() {
    return {
      top20Movies: [],
      isLoading: true,
    };
  },
  mounted() {
    document.title = "Cinemajoo - Top 20 Movies";
    this.fetchTopRatedMovies();
  },
  methods: {
    async fetchTopRatedMovies() {
      this.isLoading = true;
      try {
        const response = await fetch(
          "http://localhost:8000/api/movies/top-rated/"
        );
        const data = await response.json();
        if (response.ok) {
          this.top20Movies = Array.isArray(data)
            ? data.filter((movie) => movie && typeof movie === "object")
            : [];
        } else {
          console.error("Error fetching top rated movies:", data);
          this.top20Movies = [];
        }
      } catch (error) {
        console.error("Error fetching top rated movies:", error);
        this.top20Movies = [];
      } finally {
        this.isLoading = false;
      }
    },
    goToMovieDetail(movieId) {
      if (movieId) {
        this.$router.push(`/movie/${movieId}`);
      }
    },
  },
};
</script>

<style scoped>
.movie-card {
  border-radius: 8px;
  overflow: hidden;
  background-color: #1a0c33;
  border: 3px solid #561a7d;
}

.movie-poster {
  border-radius: 8px 8px 0 0;
}

.movie-title {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 3.2em;
}

.movie-summary {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.vote-average {
  font-size: 1.1em;
}

@media (max-width: 600px) {
  .movie-card {
    margin-bottom: 16px;
  }
}
</style>
