<template>
  <div>
    <Header />
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
    <v-container v-else fluid class="text-break" style="max-width: 91%">
      <v-row class="movie-grid" align="start" justify="space-between" dense>
        <!-- Left: Poster + Actions -->
        <v-col
          cols="12"
          md="3"
          class="left d-flex flex-column align-center align-md-start mb-4 mb-md-0"
        >
          <div class="poster">
            <img :src="posterUrl" alt="Poster" />
          </div>
          <div
            class="d-flex flex-row justify-center justify-md-space-around mt-3"
            style="width: 100%"
          >
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  :color="isWatched ? 'success' : 'grey'"
                  class="ma-2"
                  v-bind="attrs"
                  v-on="on"
                  @click="toggleWatched"
                >
                  <v-icon>
                    {{
                      isWatched
                        ? "mdi-check-circle"
                        : "mdi-check-circle-outline"
                    }}
                  </v-icon>
                </v-btn>
              </template>
              <span>{{ isWatched ? "Watched" : "Mark as watched" }}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  :color="isInWatchlist ? 'primary' : 'grey'"
                  class="ma-2"
                  v-bind="attrs"
                  v-on="on"
                  @click="toggleWatchlist"
                >
                  <v-icon>{{
                    isInWatchlist ? "mdi-bookmark" : "mdi-bookmark-outline"
                  }}</v-icon>
                </v-btn>
              </template>
              <span>{{
                isInWatchlist ? "Remove from Watchlist" : "Add to Watchlist"
              }}</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  :color="isLiked ? 'red' : 'grey'"
                  class="ma-2"
                  v-bind="attrs"
                  v-on="on"
                  @click="toggleLike"
                >
                  <v-icon>{{
                    isLiked ? "mdi-heart" : "mdi-heart-outline"
                  }}</v-icon>
                </v-btn>
              </template>
              <span>{{ isLiked ? "Unlike" : "Like" }}</span>
            </v-tooltip>
          </div>
        </v-col>

        <!-- Middle: Movie Info -->
        <v-col cols="12" md="5" class="mid d-flex flex-column">
          <div v-if="hasMovie">
            <h1 class="white--text">{{ movie.title }}</h1>
            <p class="grey--text mt-2">{{ releaseYear }}</p>
            <p class="white--text mt-2">Director: {{ movie.director }}</p>
            <p class="grey--text mt-2 text-break">{{ movie.summary_en }}</p>
            <div class="d-flex flex-row flex-wrap mt-2" v-if="actorList.length">
              <v-chip
                v-for="actor in actorList"
                :key="actor"
                small
                class="ma-1"
                outlined
                color="white"
              >
                {{ actor }}
              </v-chip>
            </div>
          </div>
        </v-col>

        <!-- Right: Ratings + User Rating -->
        <v-col cols="12" md="4" class="right d-flex flex-column">
          <div
            class="d-flex flex-row justify-center align-center"
            style="gap: 35px"
            v-if="hasMovie"
          >
            <div class="d-flex flex-column align-center mb-4" style="gap: 8px">
              <v-img
                src="../assets/images/tmdb.svg"
                alt="TMDB"
                height="40"
                width="40"
                style="border-radius: 100%"
              ></v-img>
              <p class="white--text text-center ma-0">
                {{ movie.vote_average.toFixed(1) }}
              </p>
            </div>
            <div class="d-flex flex-column align-center mb-4" style="gap: 8px">
              <v-img
                src="../assets/images/imdb-logo.svg"
                alt="IMDB"
                width="40"
                height="40"
                style="border-radius: 100%"
              ></v-img>
              <p class="white--text text-center ma-0">
                {{ movie.imdbRating || "N/A" }}
              </p>
            </div>
            <div class="d-flex flex-column align-center mb-4" style="gap: 8px">
              <v-img
                src="../assets/images/Rotten_Tomatoes.svg.png"
                alt="Rotten Tomatoes"
                width="40"
                height="40"
                style="border-radius: 100%"
              ></v-img>
              <p class="white--text text-center ma-0">
                {{ movie.rottenRating || "N/A" }}
              </p>
            </div>
          </div>
          <v-divider color="#561a7d"></v-divider>
          <div v-if="!isWatched" class="text-center pa-4">
            <span class="white--text mr-2"
              >You haven't watched this movie yet.</span
            >
          </div>
          <div
            v-if="isWatched"
            class="d-flex flex-column align-center mt-4 text-center"
          >
            <span class="white--text mr-2">Your rating</span>
            <v-rating
              v-model="userRating"
              :length="10"
              color="amber"
              background-color="grey darken-2"
              dense
            />
            <span class="grey--text ml-2">{{ userRating || 0 }}/10</span>
          </div>
        </v-col>
      </v-row>
    </v-container>

    <v-container v-if="hasMovie" style="max-width: 91%">
      <Comments :movieId="$route.params.id" />
    </v-container>
    <Footer />
  </div>
</template>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";
import Comments from "../components/Comments.vue";

export default {
  name: "MovieDetail",
  components: {
    Header,
    Footer,
    Comments,
  },
  data() {
    return {
      isWatched: false,
      isInWatchlist: false,
      isLiked: false,
      movie: {},
      userRating: 0,
      isLoading: false,
    };
  },
  computed: {
    posterUrl() {
      return this.movie && this.movie.poster_url
        ? this.movie.poster_url
        : "https://via.placeholder.com/300x450?text=No+Image";
    },
    releaseYear() {
      return this.movie && this.movie.release_date
        ? this.movie.release_date.split("-")[0]
        : "";
    },
    actorList() {
      if (!this.movie || !this.movie.actors) return [];
      return Array.isArray(this.movie.actors)
        ? this.movie.actors
        : this.movie.actors
            .split(",")
            .map((a) => a.trim())
            .filter(Boolean);
    },
    hasMovie() {
      return this.movie && Object.keys(this.movie).length > 0;
    },
  },
  mounted() {
    this.fetchMovie();
  },
  watch: {
    "$route.params.id"(newId, oldId) {
      if (newId !== oldId) {
        this.movie = {};
        this.fetchMovie();
        window.scrollTo(0, 0);
      }
    },
    userRating(newValue) {
      const username = JSON.parse(localStorage.getItem("user"));
      if (!username) return;
      const ratings = JSON.parse(localStorage.getItem("ratings")) || {};
      const movieId = this.$route.params.id;
      if (!ratings[username]) ratings[username] = {};
      ratings[username][movieId] = newValue;
      localStorage.setItem("ratings", JSON.stringify(ratings));
    },
  },
  methods: {
    async fetchMovie() {
      const id = this.$route.params.id;
      this.isLoading = true;
      try {
        const res = await fetch(`http://localhost:8000/api/movies/${id}/`);
        const data = await res.json();
        this.movie = data;
        if (data && data.title) {
          document.title = `Cinemajoo - ${data.title}`;
        }
        const username = JSON.parse(localStorage.getItem("user"));
        if (username) {
          const ratings = JSON.parse(localStorage.getItem("ratings")) || {};
          const watched = JSON.parse(localStorage.getItem("watched")) || {};
          const liked = JSON.parse(localStorage.getItem("liked")) || {};
          const watchlist = JSON.parse(localStorage.getItem("watchlist")) || {};
          const movieId = this.$route.params.id;
          this.userRating = ratings[username]?.[movieId] || 0;
          this.isWatched = watched[username]?.includes(movieId) || false;
          this.isLiked = liked[username]?.includes(movieId) || false;
          this.isInWatchlist = watchlist[username]?.includes(movieId) || false;
        }
        const apiKey = "9904dcbf";
        const omdbRes = await fetch(
          `https://www.omdbapi.com/?t=${encodeURIComponent(
            data.title
          )}&apikey=${apiKey}`
        );
        const omdbData = await omdbRes.json();
        this.movie.imdbRating = omdbData.imdbRating || "N/A";
        const rotten = omdbData.Ratings?.find(
          (r) => r.Source === "Rotten Tomatoes"
        );
        this.movie.rottenRating = rotten ? rotten.Value : "N/A";
      } catch (e) {
        console.error("Failed to load movie details:", e);
        this.movie = {};
      } finally {
        this.isLoading = false;
      }
    },
    toggleWatched() {
      this.isWatched = !this.isWatched;
      const username = JSON.parse(localStorage.getItem("user"));
      if (!username) return;
      let watched = JSON.parse(localStorage.getItem("watched")) || {};
      if (!watched[username]) watched[username] = [];
      const movieId = this.$route.params.id;
      const poster = this.posterUrl;
      if (this.isWatched) {
        if (!watched[username].includes(movieId)) {
          watched[username].push(movieId);
        }
        let recently =
          JSON.parse(localStorage.getItem("recentlyWatched")) || {};
        if (!recently[username]) recently[username] = [];
        recently[username] = recently[username].filter((m) => m.id !== movieId);
        recently[username].unshift({ id: movieId, poster });
        if (recently[username].length > 4) {
          recently[username] = recently[username].slice(0, 4);
        }
        localStorage.setItem("recentlyWatched", JSON.stringify(recently));
      } else {
        watched[username] = watched[username].filter((id) => id !== movieId);
        let recently =
          JSON.parse(localStorage.getItem("recentlyWatched")) || {};
        if (recently[username]) {
          recently[username] = recently[username].filter(
            (m) => m.id !== movieId
          );
          localStorage.setItem("recentlyWatched", JSON.stringify(recently));
        }
      }
      localStorage.setItem("watched", JSON.stringify(watched));
    },
    toggleWatchlist() {
      this.isInWatchlist = !this.isInWatchlist;
      const username = JSON.parse(localStorage.getItem("user"));
      if (!username) return;
      let watchlist = JSON.parse(localStorage.getItem("watchlist")) || {};
      if (!watchlist[username]) watchlist[username] = [];
      const movieId = this.$route.params.id;
      const poster = this.posterUrl;
      if (!watchlist[username].some((item) => item.id === movieId)) {
        watchlist[username].push({ id: movieId, poster: poster });
      } else {
        watchlist[username] = watchlist[username].filter(
          (item) => item.id !== movieId
        );
      }
      localStorage.setItem("watchlist", JSON.stringify(watchlist));
    },
    toggleLike() {
      this.isLiked = !this.isLiked;
      const username = JSON.parse(localStorage.getItem("user"));
      if (!username) return;
      let liked = JSON.parse(localStorage.getItem("liked")) || {};
      if (!liked[username]) liked[username] = [];
      const movieId = this.$route.params.id;
      const poster = this.posterUrl;
      if (!liked[username].some((item) => item.id === movieId)) {
        liked[username].push({ id: movieId, poster: poster });
      } else {
        liked[username] = liked[username].filter((item) => item.id !== movieId);
      }
      localStorage.setItem("liked", JSON.stringify(liked));
    },
  },
};
</script>

<style scoped>
.poster img {
  width: 100%;
  border-radius: 8px;border: 3px solid #561a7d;
}

.mid h1 {
  letter-spacing: 3px;
}

.right {
  border: 3px solid #561a7d;
  border-radius: 8px;
  padding: 10px;
  height: fit-content;
}

@media (max-width: 959px) {
  .poster {
    max-width: 220px;
  }
}
</style>
