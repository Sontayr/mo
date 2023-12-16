$(function () {


    /* ===============================================================
         PRODUCT SLIDER
      =============================================================== */
    $('.product-slider').owlCarousel({  //чтобы можно было листать фотографии товаров
        items: 1,
        thumbs: true,
        thumbImage: false,
        thumbsPrerendered: true,
        thumbContainerClass: 'owl-thumbs',
        thumbItemClass: 'owl-thumb-item'
    });


    /* ===============================================================
         PRODUCT QUNATITY
      =============================================================== */
      $('.dec-btn').click(function () {
          var siblings = $(this).siblings('input');
          if (parseInt(siblings.val(), 10) >= 1) {   //получаем десятичное число >=1
              siblings.val(parseInt(siblings.val(), 10) - 1);
          }
      });

      $('.inc-btn').click(function () {
          var siblings = $(this).siblings('input');
          siblings.val(parseInt(siblings.val(), 10) + 1);
      });


      /* ===============================================================
           TOGGLE ALTERNATIVE BILLING ADDRESS
        =============================================================== */
      $('#alternateAddressCheckbox').on('change', function () {
         var checkboxId = '#' + $(this).attr('id').replace('Checkbox', ''); //для смены флажка выбора адреса в корзине
         $(checkboxId).toggleClass('d-none');
      });

});

/* ===============================================================
        SCROLL-UP
   =============================================================== */
window.addEventListener('scroll', function(){       //регистрирует обработчик события
    var scroll = document.querySelector('.upward'); //querySelector() возвращает первый элемент в документе, соответствующий указанному селектору
    scroll.classList.toggle("active", window.scrollY>400) //если указанного класса у элемента нет, то classList.toggle, добавляет элементу этот класс
})
    function scrollTopTop(){ //ф-я для скролла страницы вверх
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        })
    }

