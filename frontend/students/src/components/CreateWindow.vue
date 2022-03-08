<template>
	<div id="create" class="mx-auto" data-aos="fade">
		<label id="label" class="form-label">ФИО:</label>
		<input v-model="stdName" type="text" style="width: 500px;height: 27px;margin-left: 5%;margin-top: 4%;">
		<label id="label" class="form-label">Группа:</label>
		<input v-model="group" type="text" style="width: 500px;height: 27px;margin-left: 5%;margin-top: 4%;">
		<label id="label" class="form-label">Курс:</label>
		<input v-model="cours" type="text" style="width: 500px;height: 27px;margin-left: 5%;margin-top: 4%;">
		<label id="label" class="form-label">Дата поступления:</label>
		<input v-model="date" type="date" style="width: 300px;margin-left: 5%;">
		<label id="label" class="form-label">Индив. план:</label>
		<input v-model="individual" type="checkbox" style="width: 20px;height: 20px;margin-left: 5%;">
		<label id="label" class="form-label">Фотография:</label>
		<input id="photo" class="float-none" type="file" style="width: 210px;margin-left: 5%;">
		<div v-on:click="createFunc()" class="mx-auto" style="height: 30px;width: 200px;background: #f2ffd8;margin-top: 4%;">
			<p class="m-auto" style="width: 55px; color: #000000;">Создать</p>
		</div>
	</div>
</template>
<script>
	export default{
		name: 'create-window',
		data(){
			return{
				stdName: '',
				group: '',
				cours: '',
				date: '',
				individual: false,
				photography: ''
			}
		},
		methods:{
			createFunc(){
				console.log('FILE INFORMATION:');
				console.log(this.$refs);
				var photo = document.getElementById('photo');
				this.photography = photo.files[0];
				console.log(this.photography)
				let formData = new FormData();
				formData.append('name', this.stdName);
				formData.append('stud_group', this.group);
				formData.append('cours', this.cours);
				formData.append('stud_date', this.date);
				formData.append('individual', this.individual);
				formData.append('photography', this.photography);
				axios.post('http://127.0.0.1:8000/students',
					formData, {
					headers: {
					'Content-Type': 'multipart/form-data'
					}},
				);
				this.$emit('closeCreateWindow');
			}
		}
	}
</script>