function obj2String(obj, arr = [], index = 0) {
  for (let item in obj) {
    arr[index++] = [item, obj[item]]
  }
  return new URLSearchParams(arr).toString()
}

function fetchData(url, options, method = 'GET') {
	const searchStr = obj2String(options);
  let initObj = {};
  if (method === 'GET') {
    url += '?' + searchStr;
    initObj = {
      method: method,
      credentials: 'include'
    }
  } else {
    initObj = {
      method: method,
      credentials: 'include',
      headers: new Headers({
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
      }),
      body: searchStr
    }
  }
  return fetch(url, initObj).then(function(res) {
    return res.json()
  }).then(function(data) {
    return data
  })
}

function GET(url, options) {
  return fetchData(url, options, 'GET')
}

function POST(url, options) {
  return fetchData(url, options, 'POST')
}

const UserRegistForm = {
	data: function() {
		return {
			message: '',
			content: '获取验证码',
			name: '',
			email: '',
			code: '',
			pwd: '',
			pwda: ''
		}
	},
	template:`
	<div class="controlform">
		<router-link to="/" class="closebtn" @click="message=''">x</router-link>
		<h2>注册</h2>
		<label>用户名</label>
		<input type="text" placeholder="请输入用户名" v-model="name" autofocus/>
		<label>邮箱</label>
		<input type="text" placeholder="请输入邮箱" v-model="email" />
		<button id="catcode" v-text="content" @click="clickTimeHandle"></button>
		<label>验证码</label>
		<input type="text" placeholder="请输入验证码" v-model="code" />
		<label>密码</label>
		<input type="password" placeholder="请输入密码" v-model="pwd" />
		<label>确认密码</label>
		<input type="password" placeholder="请再次输入密码" v-model="pwda" />
		<span class="notice" v-text="message"></span>
		<button @click="register">注册</button>
	</div>
	`,
	methods: {
		clickTimeHandle: function () {
			const btn = document.querySelector("#catcode");
			let time = 60;
			const vm = this;
			POST('/users/post_reg_code',{email: vm.email});
			const interval = setInterval(function() {
				if (!time) {
					btn.removeAttribute('disabled');
					vm.content = "获取验证码";
					time = 60;
					clearInterval(interval);
					return;
				}
				btn.setAttribute('disabled', true);
				vm.content = "重新发送"+time+"s";
				time--;
			},1000)
		},
		register: function() {
			const vm =this;
			if (!vm.name || !vm.email || !vm.pwd || !vm.pwda) {
				vm.message = " 输入项不能为空";
				return;
			};
			if (vm.pwd !== vm.pwda) {
				vm.message = "两次输入密码不一致";
				return;
			}
			POST('/users/register', {
				username: vm.name, 
				email: vm.email, 
				code: vm.code, 
				password: vm.pwd})
			.then(function(res) {
				if (res.response === 'ok') {
					vm.$emit("regist","注册成功，请注意查收邮件并激活帐号后登录");
					vm.$router.push('/');
				} else {
					vm.message = res.message;
				}
			})
			
		}
	}
}

const UserLoginForm = {
	data: function() {
		return {
			message: '',
			email: '',
			pwd: ''
		}
	},
	template:`
	<div class="controlform">
		<router-link to="/" class="closebtn" @click="message=''">x</router-link>
		<h2>登录</h2>
		<label>邮箱</label>
		<input type="text" placeholder="请输入邮箱" v-model="email" autofocus/>
		<label>密码</label>
		<input type="password" placeholder="请输入密码" v-model="pwd"/>
		<router-link to="/forget">忘记密码?</router-link>
		<span class="notice" v-text="message"></span>
		<button @click="login">登录</button>
	</div>
	`,
	methods: {
		login: function() {
			const vm = this;
			POST('/users/login', {email: vm.email, password: vm.pwd})
			.then(function(res) {
				if( res.response === 'ok') {
						vm.$emit('logintag', vm.email);
						vm.$router.push('/');
				} else {
					vm.message = res.message;
				}
			})
		}
	}
}

const UserForgetPWD = {
	data: function() {
		return {
			message: '',
			content: '获取验证码',
			email: '',
			code: '',
			pwd: '',
			pwda: ''
		}
	},
	template:`
	<div class="controlform">
		<router-link to="/" class="closebtn" @click="message=''">x</router-link>
		<h2>重置密码</h2>
		<label>邮箱</label>
		<input type="text" placeholder="请输入邮箱" v-model="email" autofocus/>
		<button id="catchcode" v-text="content" @click="clickTimeHandle"></button>
		<label>验证码</label>
		<input type="text" placeholder="请输入验证码" v-model="code" />
		<label>密码</label>
		<input type="text" placeholder="请输入密码" v-model="pwd" />
		<label>确认密码</label>
		<input type="text" placeholder="请再次输入密码" v-model="pwda" />
		<span class="notice" v-text="message"></span>
		<button @click="reset">确定</button>
	</div>
	`,
	methods: {
		clickTimeHandle: function () {
			const btn = document.querySelector("#catchcode");
			let time = 60;
			const vm = this;
			POST('/users/reset',{email: vm.email});
			const interval = setInterval(function() {
				if (!time) {
					btn.removeAttribute('disabled');
					vm.content = "获取验证码";
					time = 60;
					clearInterval(interval);
					return;
				}
				btn.setAttribute('disabled', true);
				vm.content = "重新发送"+time+"s";
				time--;
			},1000)
		},
		reset: function() {
			const vm = this;
			if (vm.pwd !== vm.pwda) {
				vm.message = "两次输入密码不一致";
				return;
			}
			POST('/users/post_reset', { email: vm.email, code: vm.code, password: vm.pwd})
			.then(function(res) {
				if (res.response === 'ok') {
					vm.$emit('reset', '密码重置成功，请重新登录');
					vm.$router.push('/');
				} else {
					vm.message = res.message;
				}
			})
		}
	}
}

const UserProfile = {
	props: ['info'],
	data: function() {
		return {
			img: '',
			inf: {}
		}
	},
	template:`
	<div class="editform">
		<router-link to="/" class="closebtn">x</router-link>
		<h2>Your Profile</h2>
		<router-link to="/editprofile">edit</router-link>
		<table>
			<tbody>
				<tr v-for="(value,key) in inf">
					<td>{{key}}</td>
					<td>{{value}}</td>
				</tr>
			</tbody>
		</table>
		<img :src="img" />
	</div>
	`,
	created: function() {
			const datas = Object.assign({}, this.info);
			delete datas.is_superuser;
			delete datas.image;
			this.inf = datas;
			this.img = "/media/"+this.info.image;
	}
}

const UserEditProfile = {
	props: ['info'],
	data: function() {
		return {
			message: '',
			email: '',
			username: '',
			fname: '',
			lname: '',
			address: '',
			mobile: '',
			gender: ''
		}
	},
	template:`
	<div class="editform">
		<router-link to="/" class="closebtn">x</router-link>
		<h2>Edit Your Profile</h2>
		<table>
			<tbody>
				<tr>
					<td>username</td>
					<td><input v-model="username"/></td>
				</tr>
				<tr>
					<td>first_name</td>
					<td><input v-model="fname"/></td>
				</tr>
				<tr>
					<td>last_name</td>
					<td><input v-model="lname"/></td>
				</tr>
				<tr>
					<td>address</td>
					<td><input v-model="address"/></td>
				</tr>
				<tr>
					<td>mobile</td>
					<td><input v-model="mobile"/></td>
				</tr>
				<tr>
					<td>gender</td>
					<td>
						<select v-model="gender">
							<option disabled value="">请选择</option>
							<option>male</option>
							<option>female</option>
						</select>
					</td>
				</tr>
			</tbody>
		</table>
		<button @click="editProfile">确定</button>
	</div>
	`,
	created: function() {
			const datas = Object.assign({}, this.info);
			delete datas.is_superuser;
			delete datas.image;
			this.email = datas.email;
			this.username = datas.username;
			this.fname = datas.first_name;
			this.lname = datas.last_name;
			this.address = datas.address;
			this.mobile = datas.mobile;
			this.gender = datas.gender
	},
	methods: {
		editProfile: function() {
			const vm = this;
			if (!vm.username) {
				vm.message = "用户名不能为空";
				return;
			}
			POST('/users/info', { 
				email: vm.email, 
				username: vm.username, 
				first_name: vm.fname, 
				last_name: vm.lname, 
				address: vm.address, 
				mobile: vm.mobile, 
				gender: vm.gender})
			.then(function(res) {
				if (res.response === 'ok') {
					
					vm.$emit('logintag', vm.email);
					vm.$emit('editprofile', '信息修改成功');
					vm.$router.push('/');
				} else {
					vm.message = res.message;
				}
			})
		}	
	}
}

const UsersList = {
	props: ['list','pages'],
	data: function() {
		return {
			userlist: [],
			search: '',
			nums: 1
		}
	},
	template:`
	<div class="editform">
		<router-link to="/" class="closebtn">x</router-link>
		<h3>Edit users list</h3>
		<input class="search" type="text" v-model="search" placeholder="请输入关键字搜索" autofocus />
		<table>
			<tbody>
				<tr v-for="(item,index) in userlist" :key="index">
					<td>{{index + 1}}</td>
					<td>{{item.username}}</td>
					<td>{{item.email}}</td>
				</tr>
			</tbody>
		</table>
		<ul class="pages">
			<li v-for="item in nums" v-if="nums > 1">
				<a v-text="item" @click.prevent.stop="pager"></a>
			</li>
		</ul>
	</div>
	`,
	created: function() {
		const vm = this;
		vm.userlist = vm.list.concat();
		vm.nums = vm.pages;
	},
	watch: {
		search: function() {
			const vm = this;
			GET('/users/info',{search: vm.search}).then(function(res) {
				if (res.response === 'ok') {
					vm.userlist = res.data;
					vm.nums = res.nums;
				}
			})
		}
	},
	methods: {
		pager: function(event) {
			const vm = this;
			const page = event.target.firstChild.nodeValue;
			GET('/users/info',{p:page,search:vm.search}).then(function(res) {
				if (res.response === 'ok') {
					vm.userlist = res.data;
					vm.nums = res.nums;
				}
			})
		}
	}
}

const router = new VueRouter({
	mode: 'history',
	routes: [
		{
			path: '/regist',
			component: UserRegistForm
		}, 
		{
			path: '/login',
			component: UserLoginForm
		}, 
		{
			path: '/forget',
			component: UserForgetPWD
		},
		{
			path: '/profile',
			component: UserProfile
		}, 
		{
			path: '/editprofile',
			component: UserEditProfile
		}, 
		{
			path: '/list',
			component: UsersList
		}
	]
})




const app = new Vue({
	router: router,
	el: '#app',
	data: {
		logined: false,
		msg: '',
		is_super: false,
		nums: 1,
		userinfo: {},
		userlist: []
	},
	watch: {
		msg: function () {
			const vm = this;
			if (vm.msg !== '') {
				setTimeout(function() {
					vm.msg = '';
				},1000)
			}
		}
	},
	methods: {
		logout: function() {
			this.logined = false;
		},
		handleLogin: function(email) {
			const vm = this;
			vm.msg = '';
			GET('/users/info', {email:email})
			.then(function(res) {
				if (res.response === 'ok') {
					vm.nums = res.nums;
					vm.userinfo = res.data instanceof Array ? res.data[0] : res.data;
					if (res.data instanceof Array) vm.userlist = res.data;
					vm.logined = true;
					vm.is_super = vm.userinfo.is_superuser;
				} else {
					vm.msg = res.message;
				}
			})
		},
		handleRegist: function(message) {
			this.msg = message;
		},
		handleReset: function(message) {
			this.msg = message;
		},
		handleEditProfile: function(message) {
			this.msg = message;
		}
	}
})













