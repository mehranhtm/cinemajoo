import Register from '@/views/Register'
import Login from '@/views/Login'
import Profile from '@/views/Profile'
import MovieDetail from '@/views/MovieDetail.vue'

export default [
    { path: '/', component: Register },
    { path: '/login', component: Login },
    { path: '/profile', component: Profile },
    { path: '/movie/:id', component: MovieDetail },
]