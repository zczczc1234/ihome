function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}
 $("#form-avatar").submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/user/avatar/',
        dataTyle:'json',
        type:'PATCH',
        success:function(data){
            $('#user-avatar').attr('src','/static/media/'+data.data)
        }
    })
  })


 $("#form-name").submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/user/name/',
        dataType:'json',
        type:'PATCH',
        success:function(data){
            location.href = '/user/my/'
        }

    })

 })

