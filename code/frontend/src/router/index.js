import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import register from '@/views/register.vue'
import login from '@/views/login.vue'
import cust_dash from '@/views/CustomerDashboard.vue'

import adminLogin from '@/views/adminLogin.vue'
import adminDash from '@/views/AdminDashboard.vue'
import ServiceProviders from '@/views/ServiceProviders.vue'

import AdminSummary from '@/views/AdminSummary.vue'
import SearchResults from '@/views/SearchResults.vue'
import CustomerSummary from '@/views/CustomerSummary.vue'
import professionaldashboard from '@/views/ProfessionalDashboard.vue'
import ProfessionalSummary from '@/views/ProfessionalSummary.vue'
import UserList from '@/views/UserList.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/test',
    name: 'testroute',
    component: () => import(/* webpackChunkName: "test" */ '../views/test.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: register
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/login.vue')
  },
  {
    path: '/cust_dash',
    name: 'cust_dash',
    component: cust_dash
  },
  {
    path: '/professionaldashboard',
    name: 'professionaldashboard',
    component: professionaldashboard // Updated route
  },
  {
    path: '/adminLogin',
    name: 'adminLogin',
    component: adminLogin
  },
  {
    path: '/adminDashboard',
    name: 'adminDashboard',
    component: adminDash
  },
  {
    path:'/service-providers',
    name:'service-providers',
    component:ServiceProviders
  },
  {
    path: '/customer-summary',
    name: 'customer-summary',
    component: CustomerSummary
  },
  {
    path: '/AdminSummary',
    name: 'AdminSummary',
    component: AdminSummary
  },
  {
    path: '/SearchResults',
    name: 'SearchResults',
    component: SearchResults
  },
  {
    path: '/professional-summary',
    name: 'professional-summary',
    component: ProfessionalSummary
  },
  {
    path: '/UserList',
    name: 'UserList',
    component: UserList
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
