<template>
  <v-container class="d-flex justify-center">
    <v-card
      class="signin-card rounded pa-4 d-flex flex-row mt-14"
      color="#2c1750"
    >
      <div class="pic-left">
        <img src="../assets/images/Posters.jpg" alt="Posters" />
      </div>
      <div class="right d-flex flex-column">
        <div class="d-flex flex-row title">
          <img
            src="../assets/images/logo1.png"
            alt="logo-img"
            class="rounded"
          />
          <h1 class="white--text">Cinemajoo</h1>
        </div>
        <v-card-text>
          <p class="white--text">Login to your account</p>
          <v-form ref="form">
            <v-text-field
              outlined
              label="Username"
              v-model="user.username"
              color="white"
              dark
              prepend-inner-icon="mdi-account"
              :rules="usernameRules"
            />
            <v-text-field
              outlined
              label="Password"
              v-model="user.password"
              color="white"
              dark
              prepend-inner-icon="mdi-lock"
              :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append="togglePassword"
              :rules="passwordRules"
              :type="showPassword ? 'text' : 'password'"
              class="mt-4"
            />
            <v-alert v-if="errorMessage" type="error" dense class="mt-2">
              {{ errorMessage }}
            </v-alert>
            <v-btn
              class="btn-signin mt-4"
              @click="handleLogin"
              :loading="isLoading"
            >
              Login
            </v-btn>
            <p class="white--text mt-4" style="letter-spacing: 3px">
              IF YOU DON'T HAVE AN ACCOUNT,
              <router-link
                class="text-decoration-none text-primary font-weight-bold"
                to="/"
                >REGISTER</router-link
              >
              FIRST
            </p>
          </v-form>
        </v-card-text>
      </div>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "Login",
  mounted() {
    document.title = "Cinemajoo - Login ";
  },
  data() {
    return {
      user: {
        username: "",
        password: "",
      },
      showPassword: false,
      isValid: false,
      errorMessage: "",
      isLoading: false,
      usernameRules: [
        (v) => !!v || "Username is required",
        (v) => v.length >= 4 || "Username must be at least 4 characters",
      ],
      passwordRules: [
        (v) => !!v || "Password is required",
        (v) => v.length >= 8 || "Password must be at least 8 characters",
        (v) =>
          /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,}$/.test(
            v
          ) ||
          "Password must contain uppercase, lowercase, number and special character",
      ],
    };
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    async handleLogin() {
      this.errorMessage = "";
      if (!this.$refs.form.validate()) {
        this.errorMessage = "Please fill in the fields correctly";
        return;
      }
      this.isLoading = true;
      try {
        const response = await fetch("http://127.0.0.1:8000/api/login/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.user),
        });
        if (!response.ok) {
          const errorData = await response.json();
          this.errorMessage = errorData?.detail || "Login failed.";
          return;
        }
        this.$router.push("/profile");
      } catch (error) {
        console.error("Error:", error);
        this.errorMessage = "Server not responding. Try again later.";
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.signin-card {
  width: 75%;
  gap: 20px;
}

.pic-left {
  width: 50%;
}

.right {
  width: 50%;
}

.btn-signin {
  background-color: #561a7d !important;
  color: white !important;
  width: 100%;
}

.pic-left img {
  width: 100%;
  border-radius: 8px;
}

.title img {
  width: 13%;
  fill: white;
}

.title {
  gap: 10px;
}
</style>
