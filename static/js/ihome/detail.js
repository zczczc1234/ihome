function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){

    var id = location.search.split('=')[1]
    $.ajax({
        url:'/house/detail/'+id,
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            for(var i=0; i<data.data[0].images.length; i++){
                var li = '<li class="swiper-slide"><img src="/static/media/'+data.data[0].images[i]+'"></li>'
                $('.swiper-wrapper').append(li)
            }
             var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
             })
              $(".book-house").show();
              $('.book-house').attr('href','/order/booking/?id='+data.data[0].id+'/')
        }
    })
})
