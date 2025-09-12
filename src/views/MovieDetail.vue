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
    <v-container v-else class="d-flex flex-row text-break" style="gap: 15px">
      <div class="left d-flex flex-column">
        <div class="poster">
          <img :src="posterUrl" alt="Poster" />
        </div>
        <div class="d-flex flex-row justify-space-around">
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
                    isWatched ? "mdi-check-circle" : "mdi-check-circle-outline"
                  }}</v-icon
                >
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
      </div>
      <div class="mid d-flex flex-column" v-if="hasMovie">
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
      <div class="right d-flex flex-column" style="width: 100%">
        <div
          class="d-flex flex-row justify-center align-center"
          style="gap: 35px"
          v-if="hasMovie"
        >
          <p class="white--text text-center">
            Vote Average <br />
            {{ movie.vote_average }}
          </p>
          <p class="white--text text-center">
            Vote <br />
            {{ movie.vote_average }}
          </p>
          <p class="white--text text-center">
            Vote <br />
            {{ movie.vote_average }}
          </p>
        </div>
        <v-divider color="#561a7d"></v-divider>
        <div class="d-flex flex-column align-center mt-4">
          <span class="white--text mr-2 text-center">Your rating</span>
          <v-rating
            v-model="userRating"
            :length="10"
            color="amber"
            background-color="grey darken-2"
            dense
          />
          <span class="grey--text ml-2">{{ userRating || 0 }}/10</span>
        </div>
      </div>
    </v-container>
    <Footer />
  </div>
</template>

<script>
import Header from "../components/Header.vue";
import Footer from "../components/Footer.vue";

export default {
  name: "MovieDetail",
  components: {
    Header,
    Footer,
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
        this.userRating = 0;
        this.fetchMovie();
        window.scrollTo(0, 0);
      }
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
      } catch (e) {
        console.error("Failed to load movie details:", e);
        this.movie = {};
      } finally {
        this.isLoading = false;
      }
    },
    toggleWatched() {
      this.isWatched = !this.isWatched;
      this.updateMovieStatus();
    },
    toggleWatchlist() {
      this.isInWatchlist = !this.isInWatchlist;
      this.updateMovieStatus();
    },
    toggleLike() {
      this.isLiked = !this.isLiked;
      this.updateMovieStatus();
    },
    async updateMovieStatus() {
      const id = this.$route.params.id;
      try {
        const response = await fetch(
          `http://localhost:8000/api/movies/${id}/status/`,
          {
            method: "POST", // یا PUT بسته به API شما
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              watched: this.isWatched,
              watchlist: this.isInWatchlist,
              liked: this.isLiked,
            }),
          }
        );

        if (!response.ok) {
          throw new Error("Failed to update movie status");
        }

        const data = await response.json();
        console.log("Status updated successfully:", data);
      } catch (error) {
        console.error("Error updating movie status:", error);
      }
    },
  },
};
</script>

<style scoped>
.poster {
  width: 300px;
  height: 400px;
  border: 3px solid #561a7d;
  border-radius: 8px;
}

.poster img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
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
</style>
