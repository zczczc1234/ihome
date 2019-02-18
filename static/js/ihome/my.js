function logout() {
    $.get("/user/logout/", function(data){
        console.log(data)
        if (data.code == 200) {
            location.href = "/user/login/"
        }
    })
}

$(document).ready(function(){
    $.ajax({
        url:'/user/my_message/',
        type:'GET',
        dataType:'json',
        success:function(data){
            $('#user-name').html(data.data.name)
            $('#user-mobile').html(data.data.phone)
            $('#user-avatar').attr('src','/static/media/'+data.data.avatar)
        }
    })
})