import Vue from 'vue'
import Router from 'vue-router'
import Students from '@/components/Students'
import Sections from '@/components/Sections'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'StudentsTable',
      component: Students
    },
	{
      path: '/sections',
      name: 'SectionsTable',
      component: Sections
    }
  ]
})
