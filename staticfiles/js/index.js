import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import { CardPlugin, TablePlugin } from 'bootstrap-vue'


// Make BootstrapVue available throughout your project
Vue.use(BootstrapVue)
// Add the plugins to Vue
Vue.use(CardPlugin)
Vue.use(TablePlugin)

// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)