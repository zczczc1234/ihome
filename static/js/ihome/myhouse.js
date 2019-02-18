$(document).ready(function(){
    $(".auth-warn").show();
})

function myhouse(){
    $.ajax({
        url:'/house/my_myhouse/',
        dataType:'json',
        type:'GET',
        success:function(data){
            if(data.code == 200){
                console.log(data)
                $('.auth-warn').hide()
                for(var i=0; i<data.data.length; i++){
                    var li = '<li><a href="/house/detail/?id='+data.data[i].id+'/"><div class="house-title"><h3>房屋ID:'+data.data[i].id+'--'+data.data[i].title+'</h3></div><div class="house-content"><img src="/static/media/'+data.data[i].image+'"><div class="house-text"><ul><li>位于:'+data.data[i].area+'</li><li>价格：￥'+data.data[i].price+'/晚</li><li>发布时间：'+data.data[i].create_time+'</li></ul></div></div></a></li>'
                    $('#houses-list').append(li)
                }
            }else{
                $('#houses-list').hide()
            }
        }
    })
}
myhouse()

