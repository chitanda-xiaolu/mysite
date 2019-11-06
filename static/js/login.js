var navItem = new Vue({
    el: '#navItems',
    data: {
        topmenu:[],
        userName: '',
        passWord: '',
    },
    mounted(){
        this.getData();
        this.userLogin();
    },
    methods: {
        getData: function(){
            var self = this;
            reqwest({
                url: '/index/api',
                method: 'get',
                type: 'json',
                success: function(data){
                    self.topmenu = data.navitemData;
                }
            })
        },
        userLogin: function(){
            var self = this;
            reqwest({
                url: '/index/api',
                method: 'post',
                type: 'json',
                headers: {
                    "X-CSRFTOKEN": csrfToken,
                },
                data: {
                    username: self.userName,
                    password: self.passWord,
                },
                success: function(data){
                    console.log('login success')
                    if(data.skip){
                        window.location.href='/tandacms';
                    }
                },
                error: function(err){
                    console.log(err)
                }
            })
        },
    }
})
