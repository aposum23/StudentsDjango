<template>
	<div id="create" class="mx-auto" data-aos="fade">
		<label id="label" class="form-label">ФИО:</label>
		<select v-model="stdName" style="width: 500px;height: 27px;margin-left: 5%;margin-top: 4%;">
			<option v-for="stud in students_inform" v-bind:value="stud['id']">{{stud['name']}}</option>
		</select>
		<label id="label" class="form-label">Секция:</label>
		<select v-model="sections" style="width: 500px;height: 27px;margin-left: 5%;margin-top: 4%;">
			<option v-for="sect in sections_list" v-bind:value="sect['id']">{{sect['section']}}</option>
		</select>
		<div v-on:click="createFunc()" class="mx-auto" style="height: 30px;width: 200px;background: #f2ffd8;margin-top: 4%;">
			<p class="m-auto" style="width: 55px; color: #000000;">Создать</p>
		</div>
	</div>
</template>
<script>
	var APP_LOG_LIFECYCLE_EVENTS = true;

	export default{
		name: 'create-sections',
		data(){
			return{
				stdName: '',
				sections: '',
				sections_list: [],
				students_inform: []
			}
		},
		methods:{
			createFunc(){
				let formData = new FormData();
				axios.post('http://127.0.0.1:8000/student-sections',
					{student: this.stdName,
					section: this.sections},
					);
				this.$emit('closeCreateWindow');
			}
		},
		created:
			function(){
				if (APP_LOG_LIFECYCLE_EVENTS){
					axios.get('http://127.0.0.1:8000/sections').then(response => (this.sections_list = response.data));
					axios.get('http://127.0.0.1:8000/students').then(response => (this.students_inform = response.data));
				};
			}
	}
</script>