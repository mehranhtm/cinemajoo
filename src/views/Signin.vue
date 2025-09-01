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
        <h1 class="white--text">Cinemajoo</h1>
        <v-card-text>
          <p class="white--text">Sign in to your account</p>
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
            <v-alert v-if="successMessage" type="success" dense class="mt-2">
              {{ successMessage }}
            </v-alert>
            <v-btn
              class="btn-signin mt-4"
              @click="handleSignIn"
              :loading="isLoading"
              :disabled="isLoading"
            >
              {{ isLoading ? "Signing in..." : "Sign in" }}
            </v-btn>
            <v-btn
              class="btn-register mt-2"
              @click="showRegisterForm = !showRegisterForm"
              text
              color="white"
            >
              {{ showRegisterForm ? "Already have an account? Sign in" : "Don't have an account? Register" }}
            </v-btn>
            
            <!-- Registration Form -->
            <v-expand-transition>
              <div v-if="showRegisterForm" class="mt-4">
                <v-divider class="white--text mb-4"></v-divider>
                <v-text-field
                  outlined
                  label="Email"
                  v-model="registerUser.email"
                  color="white"
                  dark
                  prepend-inner-icon="mdi-email"
                  :rules="emailRules"
                />
                <v-text-field
                  outlined
                  label="First Name"
                  v-model="registerUser.first_name"
                  color="white"
                  dark
                  prepend-inner-icon="mdi-account"
                />
                <v-text-field
                  outlined
                  label="Last Name"
                  v-model="registerUser.last_name"
                  color="white"
                  dark
                  prepend-inner-icon="mdi-account"
                />
                <v-text-field
                  outlined
                  label="Confirm Password"
                  v-model="registerUser.confirm_password"
                  color="white"
                  dark
                  prepend-inner-icon="mdi-lock-check"
                  :append-icon="showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append="toggleConfirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  :rules="confirmPasswordRules"
                />
                <v-btn
                  class="btn-register-submit mt-4"
                  @click="handleRegister"
                  :loading="isRegistering"
                  :disabled="isRegistering"
                  block
                >
                  {{ isRegistering ? "Creating account..." : "Create Account" }}
                </v-btn>
              </div>
            </v-expand-transition>
          </v-form>
        </v-card-text>
      </div>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: "Signin",
  mounted() {
    document.title = "Cinemajoo - Sign In ";
  },
  data() {
    return {
      user: {
        username: "",
        password: "",
      },
      registerUser: {
        username: "",
        email: "",
        password: "",
        confirm_password: "",
        first_name: "",
        last_name: "",
      },
      showPassword: false,
      showConfirmPassword: false,
      showRegisterForm: false,
      isLoading: false,
      isRegistering: false,
      isValid: false,
      errorMessage: "",
      successMessage: "",
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
      emailRules: [
        (v) => !!v || "Email is required",
        (v) => /.+@.+\..+/.test(v) || "Email must be valid",
      ],
      confirmPasswordRules: [
        (v) => !!v || "Please confirm your password",
        (v) => v === this.registerUser.password || "Passwords don't match",
      ],
    };
  },
  watch: {
    'registerUser.password'() {
      // Update confirm password validation when password changes
      this.$refs.form && this.$refs.form.validate();
    }
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    toggleConfirmPassword() {
      this.showConfirmPassword = !this.showConfirmPassword;
    },
    async handleSignIn() {
      this.errorMessage = "";
      this.successMessage = "";
      
      if (!this.$refs.form.validate()) {
        this.errorMessage = "Please fill in the fields correctly";
        return;
      }

      this.isLoading = true;

      try {
        const response = await fetch("http://localhost:8000/api/login/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.user),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          this.errorMessage = data.error || data.message || "Sign in failed!";
          return;
        }

        // Store tokens and user data
        localStorage.setItem("access_token", data.tokens.access);
        localStorage.setItem("refresh_token", data.tokens.refresh);
        localStorage.setItem("user", JSON.stringify(data.user));
        
        this.successMessage = "Login successful! Redirecting...";
        
        // Redirect after successful login
        setTimeout(() => {
          // this.$router.push("/dashboard");
          console.log("User logged in successfully:", data.user);
        }, 1500);
        
      } catch (error) {
        console.error("Login error:", error);
        this.errorMessage = "Server error, please try again later!";
      } finally {
        this.isLoading = false;
      }
    },
    async handleRegister() {
      this.errorMessage = "";
      this.successMessage = "";
      
      // Set username from the main form
      this.registerUser.username = this.user.username;
      
      if (!this.$refs.form.validate()) {
        this.errorMessage = "Please fill in all required fields correctly";
        return;
      }

      this.isRegistering = true;

      try {
        const response = await fetch("http://localhost:8000/api/accounts/register/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(this.registerUser),
        });
        
        const data = await response.json();
        
        if (!response.ok) {
          this.errorMessage = data.error || data.message || "Registration failed!";
          return;
        }

        this.successMessage = "Account created successfully! You can now sign in.";
        this.showRegisterForm = false;
        
        // Clear registration form
        this.registerUser = {
          username: "",
          email: "",
          password: "",
          confirm_password: "",
          first_name: "",
          last_name: "",
        };
        
        // Clear main form
        this.user = {
          username: "",
          password: "",
        };
        
        this.$refs.form.reset();
        
      } catch (error) {
        console.error("Registration error:", error);
        this.errorMessage = "Server error, please try again later!";
      } finally {
        this.isRegistering = false;
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

.btn-register {
  width: 100%;
}

.btn-register-submit {
  background-color: #2c1750 !important;
  color: white !important;
}

.pic-left img {
  width: 100%;
  border-radius: 8px;
}
</style>
