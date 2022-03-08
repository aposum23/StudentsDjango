<template>
	<div>
		<div v-on:click="changePage('students')" id="button" class="d-inline-block">
			<p class="mx-auto">Информация о студентах</p>
		</div>
		<div v-on:click="changePage('Sections')" id="button" class="d-inline-block">
			<p class="mx-auto">Информация по секциям</p>
		</div>
	</div>
</template>
<script>
	export default{
		name: 'my-header',
		data(){
			return{
				page: 'Students'
			}
		},
		methods:{
			changePage(p){
				if (this.page == p){
					return;
				}
				else if (p == 'Sections'){
					this.page = p;
					this.$router.push({name:'SectionsTable'});
				}
				else{
					this.page = p;
					this.$router.push({name:'StudentsTable'});
				}
			}
		}
	}
</script>