function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}




 $('#form-auth').submit(function(e){
        e.preventDefault();
        $(this).ajaxSubmit({
            url:'/user/my_auth/',
            dataType:'json',
            type:'PATCH',
            success:function(data){
                console.log(data)
                if(data.code == 200){
                    $('#btn').hide()
                    $('#id-card').attr("disabled",true)
                    $('#real-name').attr("disabled",true)
                }
                if(data.code == 1002){
                    $('.error-msg i').html(data.msg)
                    $('.error-msg').show()
                }
                 if(data.code == 1003){
                    $('.error-msg i').html(data.msg)
                    $('.error-msg').show()
                }

            }
        })
 })

  function auth(){
         $.ajax({
            url:'/user/my_auth/',
            dataType:'json',
            type:'GET',
            success:function(data){
                if(data.code == 200){
                    $('#id-card').val(data.data.id_card)
                    $('#real-name').val(data.data.id_name)
                    $('#btn').hide()
                    $('#id-card').attr("disabled",true)
                    $('#real-name').attr("disabled",true)
                }
            }
        })
  }
  auth()
