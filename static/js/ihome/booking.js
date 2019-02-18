function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    var id = location.search.split('=')[1]
    $.ajax({
        url:'/order/my_booking/'+id,
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            var node = '<img src="/static/media/'+data.data.image+'"> <div class="house-text"><h3>'+data.data.title+'</h3><p>￥<span>'+data.data.price+'</span>/晚</p>'
            $('.house-info').append(node)
        }
    })
})

function submit_order(){
    id = location.search.split('=')[1]
    var startDate = $("#start-date").val();
    var endDate = $("#end-date").val();
    var price = $(".house-text>p>span").html();
    var sd = new Date(startDate);
    var ed = new Date(endDate);
    days = (ed - sd)/(1000*3600*24) + 1;
    var amount = days * parseFloat(price);
    console.log(days,price,amount)

    $.ajax({
        url:'/order/submit_order/'+id,
        dataType:'json',
        type:'POST',
        data:{'startDate':startDate,'endDate':endDate,'days':days,'price':parseFloat(price),'amount':amount},
        success:function(data){
            if(data.code == 200){
                location.href = '/order/order/'
            }
        }

    })
}
