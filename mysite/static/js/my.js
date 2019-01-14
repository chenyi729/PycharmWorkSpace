 // 鼠标划过展开子菜单
 function dropdownOpen() {

     var $dropdownLi = $(li.dropdown)
     var $dropdownA = $(a.dropdown)

     $dorpdownLi.mousemove(function () {
         $(this).addClass('open')
     }).mouseout(function () {
         $(this).removeClass('open')
     })

     $dorpdownA.mousemove(function () {
         $(this).addClass('open')
     }).mouseout(function () {
         $(this).removeClass('open')
     })

 }