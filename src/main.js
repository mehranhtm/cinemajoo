import Vue from 'vue'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'
import routes from './routers/index'
import './assets/styles/styles.css'

Vue.use(VueRouter)

const router = new VueRouter({
  mode: 'history',
  routes
});

router.beforeEach((to, from, next) => {
  const user = localStorage.getItem('user')
  const publicPages = ['/', '/login']
  const authRequired = !publicPages.includes(to.path)
  if (authRequired && !user) {
    return next('/?message=auth')
  }
  if ((to.path === '/' || to.path === '/login') && user) {
    return next('/profile')
  }
  next()
})

Vue.config.productionTip = false

new Vue({
  vuetify,
  router,
  render: h => h(App)
}).$mount('#app')
