import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'

const Home = () => import('../views/Home.vue')
const room = () => import('../views/PagesInHome/room.vue')
const Profile = () => import('../views/PagesInHome/Profile.vue')
const Scripts = () => import('../views/PagesInHome/Scripts.vue')
const LoggedOut = () => import('../views/PagesInHome/LoggedOut.vue')

const Game = () => import('../views/Game.vue')

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    component: Home,
    children: [
      {
        path: '',
        name: 'Home',
        // 先路由到loggedout，然后loggedout检查登陆状态
        redirect: 'loggedout'
      },
      {
        path: 'profile',
        component: Profile
      },
      {
        path: 'scripts',
        component: Scripts
      },
      {
        path: 'room',
        component: room
      },
      {
        path: 'loggedout',
        component: LoggedOut
      }
    ]
  },
  {
    path: '/game',
    component: Game
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
