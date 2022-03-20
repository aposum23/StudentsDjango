<template>
	<div id="temp">
		<my-header></my-header>
		<div id="table" class="table-responsive">
			<label id="text" class="form-label">Сортировка: </label>
			<select v-model="stud_sort" style="width: 200px;">
				<option value="null"></option>
				<option value="fio_up">ФИО по возрастанию</option>
				<option value="fio_down">ФИО по убыванию</option>
				<option value="date_up">Дата зачисления по возрастанию</option>
				<option value="date_down">Дата зачисления по убыванию</option>
			</select>
			<div v-on:click="commitSort()" id="filter_sort_but" class="d-inline-block" style="margin-left: 6%">
				<p id="filter_sort_button" class="mx-auto">Применить сортировку</p>
			</div>
			<div v-on:click="uncommitSort()" id="filter_sort_but" class="d-inline-block" style="margin-left: 2%">
				<p id="filter_sort_button" class="mx-auto">Отменить сортировку</p>
			</div>
			<table class="table">
				<thead>
					<tr>
						<th style="width: 250px;">ФИО</th>
						<th style="width: 150px;">Дата зачисления</th>
						<th style="width: 120px;">Группа</th>
						<th style="width: 100px;">№ Курса</th>
						<th style="width: 100px;">Индив. план</th>
						<th style="width: 100px;">Фотография</th>
						<th>Секции</th>
						<th style="width: 100px;">Редактировать</th>
					</tr>
				</thead>
				<tbody v-for="row in table_inform[num_of_page]">
					<tr>
						<td>{{row['name']}}</td>
						<td>{{row['stud_date']}}</td>
						<td>{{row['stud_group']}}</td>
						<td>{{row['cours']}}</td>
						<td>{{row['individual']}}</td>
						<td>{{row['photography']}}</td>
						<td>{{row['sections']}}</td>
						<td><a v-on:click="openRedact(row)">Редактировать</a></td>
					</tr>
				</tbody>
			</table>
		</div>
		<div>
			<div id="filters">
				<p id="text">Фильтры:</p>
				<label id="text" class="form-label">ФИО:</label>
				<input v-model="name" type="text" style="width: 500px;">
				<label id="text" class="form-label">Индивидуальный план:</label>
				<select v-model="individual" style="width: 200px;">
					<option value="null"></option>
					<option value="true">На инд. плане</option>
					<option value="false">На обычном</option>
				</select>
				<label id="text" class="form-label">Номер курса:</label>
				<input v-model="cours" type="text" style="width: 50px;">
				<div v-on:click="commitFilters()" id="filter_sort_but" class="d-inline-block" style="margin-left: 15%">
					<p id="filter_sort_button" class="mx-auto">Применить фильтры</p>
				</div>
				<div v-on:click="uncommitFilters()" id="filter_sort_but" class="d-inline-block" style="margin-left: 5%">
					<p id="filter_sort_button" class="mx-auto">Отменить фильтры</p>
				</div>
			</div>
			<div v-on:click="createWindow()" id="create_but" class="d-inline-block">
				<p id="create_button" class="mx-auto">Создать запись</p>
			</div>
		</div>
		<create-window v-on:closeCreateWindow="createWindow()" v-show="create_data"></create-window>
		<update-students v-on:closeRedactWindow="redactWindow()" v-show="redact"></update-students>
		<div id="pages">
			<div v-on:click="changePage(index)"  v-for="(row, index) in table_inform" id="page_num" class="float-start">
				<p class="mx-auto">{{index + 1}}</p>
			</div>
		</div>
	</div>
</template>
<script>
	import CreateWindow from './CreateWindow.vue';
	import MyHeader from './Header.vue';
	import UpdateStudents from './UpdateStudents.vue';
	
	var APP_LOG_LIFECYCLE_EVENTS = true;

	export default{
		name: 'students',
		data(){
			return{
				table_inform: [],
				name: '',
				individual: 'null',
				cours: '',
				create_data: false,
				num_of_page: 0,
				redact: false,
				row_for_redact: [],
				filter_status: false,
				stud_sort: '',
			}
		},
		components: { CreateWindow, MyHeader, UpdateStudents },
		methods:{
			openRedact(row){
				this.redactWindow();
				this.row_for_redact = row;
				this.$children[2].row = this.row_for_redact;
			},
			redactWindow(){
				this.redact =!this.redact;
				if (this.filter_status == true){
					console.log('FILTERING')
					this.commitFilters();
				}
			},
			createWindow(){
				this.create_data = !this.create_data;
			},
			mainArraysSet(array){
				this.table = array;
				this.reserv_table= array;
				this.table_inform = [];
				this.createSubArrays(this.reserv_table);
				console.log(this.reserv_table);
				return;
			},
			createSubArrays(array){
				this.table_inform = [];
				for (let i = 0; i <array.length; i += 5) {
					this.table_inform.push(array.slice(i, i + 5));
				};
				console.log(this.table_inform);
				return;
			},
			changePage(page_num){
				this.num_of_page = page_num;
			},
			commitFilters(){
				let formData = new FormData();
				formData.append('fio', this.name);
				formData.append('individual', this.individual);
				formData.append('cours', this.cours);
				axios.post('http://127.0.0.1:8000/filter-students',
					formData, {
					headers: {
					'Content-Type': 'multipart/form-data'
					}},
				).then(response => (this.mainArraysSet(response.data)));
				this.filter_status = true;
				this.num_of_page = 0;
			},
			uncommitFilters(){
				this.name = '';
				this.individual = 'null'
				this.cours = '';
				let formData = new FormData();
				formData.append('fio', this.name);
				formData.append('individual', this.individual);
				formData.append('cours', this.cours);
				axios.post('http://127.0.0.1:8000/filter-students',
					formData, {
					headers: {
					'Content-Type': 'multipart/form-data'
					}},
				).then(response => (this.mainArraysSet(response.data)));
				this.filter_status = false;
				this.num_of_page = 0;
			},
			commitSort(){
				let formData = new FormData();
				formData.append('method', this.stud_sort);
				axios.post('http://127.0.0.1:8000/sort-students',
					formData, {
					headers: {
					'Content-Type': 'multipart/form-data'
					}},
				).then(response => (this.mainArraysSet(response.data)));
			},
			uncommitSort(){
				let formData = new FormData();
				this.stud_sort = '';
				formData.append('method', this.stud_sort);
				axios.post('http://127.0.0.1:8000/sort-students',
					formData, {
					headers: {
					'Content-Type': 'multipart/form-data'
					}},
				).then(response => (this.mainArraysSet(response.data)));
			}
		},
		created:
			function(){
				if (APP_LOG_LIFECYCLE_EVENTS){
					axios.get('http://127.0.0.1:8000/students').then(response => (this.mainArraysSet(response.data)));
				}
			}
	}
</script>