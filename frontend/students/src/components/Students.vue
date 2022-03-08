<template>
	<div id="temp">
		<my-header></my-header>
		<div id="table" class="table-responsive">
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
					<input v-on:input="filterInformation(table, 'name')" v-model="name" type="text" style="width: 500px;">
					<label id="text" class="form-label">Индивидуальный план:</label>
					<select v-on:change="filterInformation(table, 'indiv')" v-model="individual" style="width: 200px;">
						<option value="null"></option>
						<option value="true">На инд. плане</option>
						<option value="false">На обычном</option>
					</select>
					<label id="text" class="form-label">Номер курса:</label>
					<input v-on:input="filterInformation(table, 'cours')" v-model="cours" type="text" style="width: 50px;">
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
	</div>
</template>
<script>
	import CreateWindow from './CreateWindow.vue';
	import MyHeader from './Header.vue';
	import UpdateStudents from './UpdateStudents.vue';
	
	var APP_LOG_LIFECYCLE_EVENTS = true;

	function boyer(S, P) {
            var ret = [];
        
            var k = P.length - 1, o = {}, l = S.length, i = 0, j, c;
            for (; i < k; i++)
                o[P.charAt(i)] = k - i;
            i = 0;
            while (i < l) {
                for (j = k; j >= 0; j--)
                    if (P.charAt(j) != S.charAt(i + j)) {
                        break;
                    }
                if (j < 0) {
                    i++;
                    ret.push(i);
                }
                else {
                    c = o[S.charAt(i + j)];
                    if (!c)
                        c = k + 1;
                    c += j - k;
                    if (c <= 0) 
                        c = 1;
                    i += c;
                }
            }
            return ret;
        };
	
	export default{
		name: 'students',
		data(){
			return{
				table: [],
				table_inform: [],
				reserv_table: [],
				name: '',
				individual: 'null',
				last_indiv: '',
				cours: '',
				create_data: false,
				num_of_page: 0,
				redact: false,
				row_for_redact: [],
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
			},
			createWindow(){
				this.create_data = !this.create_data;
				if (APP_LOG_LIFECYCLE_EVENTS){
					axios.get('http://127.0.0.1:8000/students').then(response => (this.table_inform = response.data));
				};
			},
			filterInformation(table, type){
				if (type == 'name'){
					this.filterName(table);
				}
				else if (type == 'indiv'){
					this.filterIndividual(table);
				}
				else if (type == 'cours'){
					this.filterCours(table);
				};
				this.createSubArrays(this.table);
				this.num_of_page = 0;
			},
			//Фильтр по имени студента
			filterName(reserv){
				if (this.name != ''){//Если значение имени не пустое выполняем следующее
					this.refreshInf();//Обнуляем основную таблицу
					for (let i = 0; i < reserv.length; i++){//Цикл в котором проходит поиск подстроки в строке алгоритмом Бойера-Мура
						var res = boyer(reserv[i]['name'], this.name);//Вызов алгоритма Бойера-Мура
						if (res.length > 0){//Если алгоритм вернул не пустой массив, то выполняем следующее
							this.table.push(reserv[i]);
						};
					};
				}
				else{//Если значение имени студента пустое, очищаем фильтры и применяем другие, если значения тех не пустые
					this.clearFilter();
					if(this.cours != ''){
						this.filterCours(this.table);
					};
					if(this.individual != 'null'){
						this.filterIndividual(this.table);
					};
				};
			},
			//Фильтр по индивидуальному плану
			filterIndividual(reserv){
				if (this.individual != 'null'){//Если значение индивидуального плана не 'null' то выполняем фильтрацию
					if (this.last_indiv == 'true' || this.last_indiv == 'false'){
						reserv = this.reserv_table;
					};
					this.refreshInf();//Обнуляем основную таблицу

					if (this.individual == 'true'){//Если значение индивидуальноо плана 'true' - выполняем следующее
						for (let i = 0; i < reserv.length; i++){//Проходим массив циклом
							if (reserv[i]['individual'] == true){//Если значение в массиве true, то
								this.table.push(reserv[i]);
							};
						};
						this.last_indiv = this.individual;//Сохраняем что последний фильтр по инивидуальному плану 'true'
					}
					else if (this.individual == 'false'){//Если значение индивидуального плана 'false' - выполняем следующее
						for (let i = 0; i < reserv.length; i++){//Проходим массив циклом
							if (reserv[i]['individual'] == false){//Если значение в массиве false, то
								this.table.push(reserv[i]);
							};
						};
						this.last_indiv = this.individual;//Сохраняем что последний фильтр по инивидуальному плану 'false'
					};
					if(this.name != ''){
						this.filterName(this.table);
						};
						if(this.cours != ''){
							this.filterCours(this.table);
						};
				}
				else{//Иначе мы очищаем фильтр, если другие фильтры не пустые, то применяем их
					this.clearFilter();
					if(this.name != ''){
						this.filterName(this.table);
					};
					if(this.cours != ''){
						this.filterCours(this.table);
					};
				};
			},
			//Фильтр по номеру курса студента
			filterCours(reserv){
				if (this.cours != ''){//Если значение курса не пустое, то выполняем следующее
					this.refreshInf();//Обнуляем основную таблицу

					for (let i = 0; i < reserv.length; i++){//Циклический проход массива
						if (reserv[i]['cours'] == parseInt(this.cours, 10)){//Если номер курса в массиве равен номеру курса в фильтре
							this.table.push(reserv[i]);
						};
					};
					if(this.name != ''){//Если значение фильтра имени не пустое
						//Применяем фильтр по имени
						this.filterName(this.table);
					};
					if(this.individual != 'null'){//Если значение фильтра по индивидуальному плану не пустое
					//Применяем фильтр по индивидуальному плану
						this.filterIndividual(this.table);
					};
				}
				else{//Иначе очищаем фильтр, если другие не пустые, то применяем их
					this.clearFilter();
					if(this.name != ''){
						this.filterName(this.table);
					};
					if(this.individual != 'null'){
						this.filterIndividual(this.table);
					};
				};
			},
			refreshInf(){//Функция обновления данных
				this.table_inform = [];//Очищаем основную
				this.table = [];
			},
			clearFilter(){
				this.table_inform = []
				this.mainArraysSet(this.reserv_table);
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