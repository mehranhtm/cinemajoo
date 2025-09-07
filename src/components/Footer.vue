<template>
  <v-footer color="#2c1750" class="footer">
    <v-container>
      <v-row class="text-center">
        <v-col cols="12" md="4">
          <div class="d-flex flex-column align-center">
            <div class="d-flex align-center mb-3">
              <img
                src="../assets/images/logo1.png"
                alt="logo"
                class="footer-logo"
              />
              <h3 class="white--text ml-2">Cinemajoo</h3>
            </div>
            <p class="white--text footer-description">
              Your ultimate destination for discovering and exploring movies
            </p>
          </div>
        </v-col>

        <v-col cols="12" md="4">
          <div class="d-flex flex-column align-center">
            <h4 class="white--text mb-3">Quick Links</h4>
            <!-- <div class="d-flex flex-column">
              <router-link to="/login" class="footer-link">Login</router-link>
              <router-link to="/register" class="footer-link"
                >Register</router-link
              >
              <router-link to="/profile" class="footer-link"
                >Profile</router-link
              >
            </div> -->
          </div>
        </v-col>

        <v-col cols="12" md="4">
          <div class="d-flex flex-column align-center">
            <h4 class="white--text mb-3">Connect With Us</h4>
            <div class="d-flex social-links">
              <v-btn icon color="white" class="social-btn">
                <v-icon>mdi-facebook</v-icon>
              </v-btn>
              <v-btn icon color="white" class="social-btn">
                <v-icon>mdi-twitter</v-icon>
              </v-btn>
              <v-btn icon color="white" class="social-btn">
                <v-icon>mdi-instagram</v-icon>
              </v-btn>
            </div>
          </div>
        </v-col>
      </v-row>

      <v-divider color="#561a7d" class="my-4"></v-divider>

      <v-row class="text-center">
        <v-col cols="12">
          <p class="white--text copyright">
            © {{ currentYear }} Cinemajoo. All rights reserved.
          </p>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {
      currentYear: new Date().getFullYear(),
    };
  },
};
</script>

<style scoped>
.footer {
  margin-top: auto;
}

.footer-logo {
  width: 30px;
  height: 30px;
}

.footer-description {
  font-size: 14px;
  opacity: 0.8;
  max-width: 250px;
}

.footer-link {
  color: white !important;
  text-decoration: none;
  margin-bottom: 8px;
  transition: color 0.3s ease;
  font-size: 14px;
}

.footer-link:hover {
  color: #ffd700 !important;
}

.social-links {
  gap: 12px;
}

.social-btn {
  transition: background-color 0.3s ease;
}

.social-btn:hover {
  background-color: rgba(255, 255, 255, 0.1) !important;
}

.copyright {
  font-size: 12px;
  opacity: 0.7;
  margin: 0;
}

/* Responsive design */
@media (max-width: 768px) {
  .footer-logo {
    width: 25px;
    height: 25px;
  }

  .footer-description {
    font-size: 12px;
    max-width: 200px;
  }

  .social-links {
    gap: 8px;
  }
}
</style>
