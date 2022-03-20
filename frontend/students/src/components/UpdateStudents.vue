<template>
	<div id="create" class="mx-auto" data-aos="fade">
		<label id="label" class="form-label">ФИО:</label>
		<input v-model="row.name" type="text" style="width: 500px;height: 27px;margin-left: 5%;margin-top: 4%;">
		<label id="label" class="form-label">Группа:</label>
		<input v-model="row.stud_group" type="text" style="width: 500px;height: 27px;margin-left: 5%;margin-top: 4%;">
		<label id="label" class="form-label">Курс:</label>
		<input v-model="row.cours" type="text" style="width: 500px;height: 27px;margin-left: 5%;margin-top: 4%;">
		<label id="label" class="form-label">Дата поступления:</label>
		<input v-model="row.stud_date" type="date" style="width: 300px;margin-left: 5%;">
		<label id="label" class="form-label">Индив. план:</label>
		<input v-model="row.individual" type="checkbox" style="width: 20px;height: 20px;margin-left: 5%;">
		<label id="label" class="form-label">Фотография:</label>
		<input id="redact-photo" class="float-none" type="file" style="width: 210px;margin-left: 5%;">
		<div v-on:click="createFunc()" class="mx-auto" style="height: 30px;width: 200px;background: #f2ffd8;margin-top: 4%;">
			<p class="m-auto" style="width: 55px; color: #000000;">Сохранить</p>
		</div>
		<div v-on:click="deleteRecord()" class="mx-auto" style="height: 30px;width: 200px;background: #f2ffd8;margin-top: 4%;">
			<p class="m-auto" style="width: 55px; color: #000000;">Удалить</p>
		</div>
	</div>
</template>
<script>
import { BIconArrowRightSquareFill } from "bootstrap-vue";

	export default{
		name: 'update-student',
		data(){
			return{
				photography: '',
				row: [],
			}
		},
		methods:{
			createFunc(){
				var photo = document.getElementById('redact-photo');
				this.photography = photo.files[0];
				console.log(this.photography);
				let formData = new FormData();
				formData.append('id', this.row.id);
				formData.append('name', this.row.name);
				formData.append('stud_group', this.row.group);
				formData.append('cours', this.row.cours);
				formData.append('stud_date', this.row.stud_date);
				formData.append('individual', this.row.individual);
				formData.append('photography', this.photography);
				axios.post('http://127.0.0.1:8000/update-students',
					formData, {
					headers: {
					'Content-Type': 'multipart/form-data'
					}});
				this.$emit('closeRedactWindow');
			},
			deleteRecord(){
				let formData = new FormData();
				formData.append('id', this.row.id);
				formData.append('name', '');
				formData.append('stud_group', this.row.group);
				formData.append('cours', this.row.cours);
				formData.append('stud_date', this.row.stud_date);
				formData.append('individual', this.row.individual);
				formData.append('photography', this.photography);
				axios.post('http://127.0.0.1:8000/update-students',
					formData, {
					headers: {
					'Content-Type': 'multipart/form-data'
					}});
				this.$emit('closeRedactWindow');
			},
		},
	}
</script>