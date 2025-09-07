<template>
  <div>
    <Header />
    <v-container class="mb-8">
      <div class="profile-container d-flex flex-row justify-space-between mb-8">
        <h1 class="white--text">Welcome, {{ user }}</h1>
        <p class="white--text ma-0">Total:</p>
      </div>
      <v-divider color="#561a7d"></v-divider>
      <div class="d-flex flex-row justify-space-evenly mt-8">
        <div class="favorite-movies d-flex flex-column">
          <p class="white--text mb-10">Your Favorite Movies:</p>
          <div class="d-flex flex-row" style="gap: 15px">
            <div class="favorite-movie"></div>
            <div class="favorite-movie"></div>
            <div class="favorite-movie"></div>
            <div class="favorite-movie"></div>
          </div>
        </div>
        <div class="d-flex flex-row justify-space-evenly"></div>
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
    };
  },
  mounted() {
    document.title = "Cinemajoo - Profile ";
    this.user = JSON.parse(localStorage.getItem("user"));
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
  font-size: 1.5rem;
  letter-spacing: 3px;
}

.favorite-movie {
  width: 170px;
  height: 210px;
  border: 3px solid #561a7d;
  border-radius: 8px;
}
</style>
