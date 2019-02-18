//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

    $.ajax({
        url:'/order/my_lorder/',
        dataType:'json',
        type:'GET',
        success:function(data){
            console.log(data)
            for(var i=0; i<data.data.length; i++){
                var status = data.data[i].status
                var li = '<li order-id='+data.data[i].order_id+'><div class="order-title"><h3>订单编号：'+data.data[i].order_id+
                '</h3> <div class="fr order-operate"> <button type="button" class="btn btn-success order-accept" data-toggle="modal" data-target="#accept-modal">接单</button><button type="button" class="btn btn-danger order-reject" data-toggle="modal" data-target="#reject-modal">拒单</button> </div></div> <div class="order-content"> <img src="/static/media/'+data.data[i].image+
                '"><div class="order-text"><h3>'+data.data[i].house_title+'</h3><ul><li>创建时间：'+data.data[i].create_date+
                '</li><li>入住日期：'+data.data[i].begin_date+
                '</li><li>离开日期：'+data.data[i].end_date+
                '</li><li>合计金额：'+data.data[i].amount+
                '(共'+data.data[i].days+'晚)</li><li>订单状态：<span>'+data.status[status]+
                '</li><li></li></ul></div></div></li>'
                $('.orders-list').append(li)
                if(data.data[i].status == 'REJECTED'){
                    $('.order-accept').hide()
                    $('.order-reject').hide()
                 }
                if(data.data[i].status == 'WAIT_PAYMENT'){
                        $('.order-accept').hide()
                        $('.order-reject').hide()
                }
            }

            $(".order-accept").on("click", function(){
                     var orderId = $(this).parents("li").attr("order-id");
                     $(".modal-accept").attr("order-id", orderId);

            });

             $(".order-reject").on("click", function(){
                      var orderId = $(this).parents("li").attr("order-id");
                      $(".modal-reject").attr("order-id", orderId);
             });
        }
    })
});

 $('.modal-accept').click(function(){
            var orderId  = $(".modal-accept").attr("order-id")
            var status = 'WAIT_PAYMENT'
            $.ajax({
                url:'/order/accept_order/',
                dataType:'json',
                type:'PATCH',
                data:{'orderId':orderId,'status':status},
                success:function(data){
                    location.reload()
                }
            })
 })

 $(".modal-reject").click(function(){
        var orderId =  $(".modal-reject").attr("order-id")
        var comment = $('.form-control').val()
        var status = 'REJECTED'
        $.ajax({
                url:'/order/accept_order/',
                dataType:'json',
                type:'PATCH',
                data:{'orderId':orderId,'status':status,'comment':comment},
                success:function(data){
                    location.reload()
                }
            })
 })
