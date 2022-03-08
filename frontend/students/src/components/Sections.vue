<template>
	<div id="temp">
		<my-header></my-header>
		<div id="table" class="table-responsive">
			<table class="table">
				<thead>
					<tr>
						<th style="width: 250px;">Наименование секции</th>
						<th>ФИО студента</th>
					</tr>
				</thead>
				<tbody v-for="(row, index) in table_inform[num_of_page]">
					<tr>
						<td>{{row['section']['section']}}</td>
						<td>{{row['student']['name']}}</td>
					</tr>
				</tbody>
			</table>
		</div>
		<div>
			<div id="filters">
					<p id="text">Фильтры:</p>
				<label id="text" class="form-label">ФИО:</label>
				<input v-on:input="filterName()" v-model="name" type="text" style="width: 500px;height: 27px;margin-left: 5%;margin-top: 4%;">
			</div>
			<div v-on:click="createWindow()" id="create_but" class="d-inline-block">
				<p id="create_button" class="mx-auto">Создать запись</p>
			</div>
		</div>
		<div id="pages">
				<div v-on:click="changePage(index)"  v-for="(row, index) in table_inform" id="page_num" class="float-start">
					<p class="mx-auto">{{index + 1}}</p>
				</div>
			</div>
		<create-sections v-on:closeCreateWindow="createWindow()" v-show="create_data"></create-sections>
	</div>
</template>
<script>
	import CreateSections from './CreateSections.vue';
	import MyHeader from './Header.vue';

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
		name: 'sections',
		data(){
			return{
				table_inform: [],
				table: [],
				reserv_table: [],
				create_data: false,
				name: '',
				num_of_page: 0,
			}
		},
		components: {CreateSections, MyHeader},
		methods:{
			createWindow(){
				this.create_data = !this.create_data;
				if (APP_LOG_LIFECYCLE_EVENTS){
					axios.get('http://127.0.0.1:8000/student-sections').then(response => (this.table_inform = response.data));
				}
			},
			filterName(){
				if (this.name != ''){//Если значение имени не пустое выполняем следующее
					this.table = [];//Обнуляем основную таблицу
					var leng = this.reserv_table.length;
					for (let i = 0; i < leng; i++){//Цикл в котором проходит поиск подстроки в строке алгоритмом Бойера-Мура
						var res = boyer(this.reserv_table[i]['student']['name'], this.name);//Вызов алгоритма Бойера-Мура
						if (res.length > 0){//Если алгоритм вернул не пустой массив, то выполняем следующее
							this.table.push(this.reserv_table[i]);//Иначе заносим в таблицу
						};
					};
					this.createSubArrays(this.table);

				}
				else{//Если значение имени студента пустое, очищаем фильтры и применяем другие, если значения тех не пустые
					this.clearFilter();
				};
			},
			clearFilter(){
				//this.table_inform = this.reserv_table;//Основной таблице передаём значения резервной
				this.table_inform = [];
				this.createSubArrays(this.reserv_table);
			},
			mainArraysSet(array){
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
					axios.get('http://127.0.0.1:8000/student-sections').then(response => (this.mainArraysSet(response.data)));
				}
			}
	}
</script>