function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
})

function area(){
    $.ajax({
        url:'/house/area/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            for(var i=0; i<data.data.length;i++){
                var option = document.createElement('option')
                $(option).val(data.data[i].id)
                $(option).text(data.data[i].name)
                $('#area-id').append(option)
            }
        }
    })
}
area()


function facility(){
    $.ajax({
        url:'/house/house_facility/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            for(var i=0; i<data.data.length; i++){
                var li = '<li><div class="checkbox"><label><input type="checkbox" name="facility" value="'+data.data[i].id+'">'+data.data[i].name+'</label> </div></li>'
                $('.clearfix').append(li)
            }
        }
    })
}
facility()

$('#form-house-info').submit(function(e){
    e.preventDefault();
    $(this).ajaxSubmit({
        url:'/house/house_info/',
        dataType:'json',
        type:'POST',
        success:function(data){
            if(data.code == 200){
                $('#form-house-info').hide()
                $('#form-house-image').show()
                $('#house-id').val(data.data)
            }
        }
    })
})

$('#form-house-image').submit(function(e){
       e.preventDefault()
       $(this).ajaxSubmit({
        url:'/house/house_image/',
        dataType:'json',
        type:'POST',
        success:function(data){
            var img = '<img src="/static/media/'+data.data+'">'
            $('.house-title').append(img)
        }

       })

})
