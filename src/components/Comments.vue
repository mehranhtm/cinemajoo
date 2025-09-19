<template>
  <div class="comments-section">
    <v-divider color="#561a7d" class="my-4"></v-divider>
    <h2 class="white--text mb-4">Comments</h2>
    <v-card class="mb-4" color="#2a1a4a" elevation="2">
      <v-card-text>
        <v-textarea
          v-model="newComment"
          label="Write a comment..."
          rows="3"
          auto-grow
          outlined
          color="purple"
          background-color="#1a0c33"
        ></v-textarea>
        <div class="d-flex justify-end">
          <v-btn
            color="purple"
            @click="addComment"
            :disabled="!newComment.trim()"
            class="white--text"
          >
            Post Comment
          </v-btn>
        </div>
      </v-card-text>
    </v-card>
    <div v-if="comments.length > 0" class="comments-list">
      <v-card
        v-for="(comment, index) in comments"
        :key="index"
        class="mb-3"
        color="#2a1a4a"
        elevation="2"
      >
        <v-card-text>
          <div class="d-flex align-center mb-2">
            <v-avatar size="32" color="purple" class="mr-3">
              <span class="white--text">{{
                comment.username.charAt(0).toUpperCase()
              }}</span>
            </v-avatar>
            <div>
              <h4 class="white--text ma-0">{{ comment.username }}</h4>
              <small class="grey--text">{{
                formatDate(comment.timestamp)
              }}</small>
            </div>
          </div>
          <p class="white--text ma-0">{{ comment.text }}</p>
        </v-card-text>
      </v-card>
    </div>
    <div v-else class="text-center pa-4">
      <p class="grey--text">No comments yet. Be the first to comment!</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "Comments",
  props: {
    movieId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      newComment: "",
      comments: [],
    };
  },
  computed: {
    currentUser() {
      const user = localStorage.getItem("user");
      return user ? JSON.parse(user) : null;
    },
  },
  mounted() {
    this.loadComments();
  },
  watch: {
    movieId() {
      this.loadComments();
    },
  },
  methods: {
    loadComments() {
      const comments = JSON.parse(localStorage.getItem("movieComments")) || {};
      this.comments = comments[this.movieId] || [];
    },
    addComment() {
      if (!this.newComment.trim() || !this.currentUser) return;
      const comment = {
        id: Date.now(),
        username: this.currentUser,
        text: this.newComment.trim(),
        timestamp: new Date().toISOString(),
      };
      const comments = JSON.parse(localStorage.getItem("movieComments")) || {};
      if (!comments[this.movieId]) {
        comments[this.movieId] = [];
      }
      comments[this.movieId].unshift(comment);
      localStorage.setItem("movieComments", JSON.stringify(comments));
      this.comments = comments[this.movieId];
      this.newComment = "";
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      const now = new Date();
      const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
      if (diffInHours < 1) {
        return "Just now";
      } else if (diffInHours < 24) {
        return `${diffInHours} hour${diffInHours > 1 ? "s" : ""} ago`;
      } else if (diffInHours < 48) {
        return "Yesterday";
      } else {
        return date.toLocaleDateString();
      }
    },
  },
};
</script>

<style scoped>
.comments-section {
  margin-top: 20px;
}

.comments-list {
  max-height: 500px;
  overflow-y: auto;
}

.comments-list::-webkit-scrollbar {
  width: 6px;
}

.comments-list::-webkit-scrollbar-track {
  background: #1a0c33;
}

.comments-list::-webkit-scrollbar-thumb {
  background: #561a7d;
  border-radius: 3px;
}

.comments-list::-webkit-scrollbar-thumb:hover {
  background: #7a2ba8;
}

.v-textarea >>> .v-input__control >>> .v-input__slot {
  background-color: #1a0c33 !important;
}

.v-textarea >>> .v-label {
  color: #9c27b0 !important;
}

.v-textarea
  >>> .v-input__control
  >>> .v-input__slot
  >>> .v-text-field__slot
  >>> textarea::placeholder {
  color: #9c27b0 !important;
}

.v-textarea
  >>> textarea {
    color: white !important;
}
</style>
