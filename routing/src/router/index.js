import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// import StoreManagerlogin from '../views/StoreManagerlogin.vue'
import ContactView from '../views/ContactView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import AdminloginView from '@/views/AdminloginView.vue'
import StoreView from '@/views/StoreView.vue'
import AdminPanel from '@/views/AdminPanel.vue'
import ProductPage from '@/views/ProductPage.vue'
import EditPage from '@/views/EditProduct.vue'
import EditCategory from '@/views/EditCategory.vue'
import CartViewVue from '@/views/CartView.vue'
import SmSignup from '@/views/SmSignup.vue'
import ApproveView from '@/views/ApproveView.vue'
import FilteredView from '@/views/FilteredView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/contact',
    name: 'contact',
    component: ContactView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/admin_login',
    name: 'admin_login',
    component: AdminloginView
  },
  {
    path: '/store_view',
    name: 'store_view',
    component: StoreView
  },
  {
    path: '/admin_panel',
    name: 'admin_panel',
    component: AdminPanel
  },
  {
    path: '/products',
    name: 'products',
    component: ProductPage,
  },
  {
    path: '/edit/:id',
    name: 'edit-page',
    component: EditPage,
  },
  {
    path: '/edit_category/:id',
    name: 'edit-category',
    component:EditCategory,
  },
  {
    path: '/store_ms_login',
    name: 'store_ms_login',
    component: SmSignup
  },
  {
    path: '/cart',
    name: 'cart',
    component: CartViewVue
  },
  {
    path: '/approve_sm',
    name: 'approve_sm',
    component: ApproveView
  },
  {
    path: '/filteredview',
    name: 'filteredview',
    component: FilteredView
  },
]


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (from.name === 'admin_panel' && to.name === 'admin_login') {
    next(false);
  } else {
    next();
  }
})

router.beforeEach((to, from, next) => {
  if (from.name === 'store_view' && to.name === 'store_ms_login') {
    next(false);
  } else {
    next();
  }
})

router.beforeEach((to, from, next) => {
  if (from.name === 'store_view' && to.name === 'login') {
    next(false);
  } else {
    next();
  }
})

export default router;
