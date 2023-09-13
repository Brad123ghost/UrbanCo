const swiper = new Swiper('.swiper', {
    direction: 'horizontal',
    slidesPerView: 5,
    slidesPerGroup: 5,

    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },

    navigation: {
        prevEl: '.swiper-button-prev',
        nextEl: '.swiper-button-next'
    },
});
