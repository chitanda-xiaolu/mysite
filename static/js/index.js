var navItem = new Vue({
    el: '#navItems',
    data: {
        topmenu:[],
        userName: '',
        passWord: '',
    },
    mounted(){
        this.getData();
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
                data: {
                    userName: self.userName,
                    password: self.passWord,
                },
                success: function(){
                    console.log('login success')
                },
                error: function(err){
                    console.log(err)
                }
            })
        },
    }
})

var banner = new Vue({
    el: '#imageList',
    data: {
        banner: [],
    },
    mounted(){
        this.getData();
    },
    methods: {
        getData: function(){
            var self = this;
            reqwest({
                url: '/index/api',
                method: 'get',
                type: 'json',
                success: function(data){
                   self.banner = data.bannerData;
                }
            })
        }
    }
})

var article = new Vue({
    el: '#blogItem',
    data: {
        articleItems: [],
    },
    mounted(){
        this.getData();
    },
    methods: {
        getData: function(){
           var self = this;
           reqwest({
               url: '/index/api',
               method: 'get',
               type: 'json',
               success: function(data){
                   console.log(data.articleData)
                   self.articleItems = data.articleData;
               }
           })
        }
    },
})