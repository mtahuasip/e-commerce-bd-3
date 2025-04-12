$(document).ready(function () {
  $(".navbar-burger").on("click", function (e) {
    e.stopPropagation();
    $(".navbar-burger").toggleClass("is-active");
    $(".navbar-menu").toggleClass("is-active");
  });

  $(".dropdown").on("click", function (e) {
    e.stopPropagation();
    $(".dropdown").not(this).removeClass("is-active");
    $(this).toggleClass("is-active");
  });

  $(document).on("click", function () {
    $(".dropdown").removeClass("is-active");
    $(".navbar-burger").removeClass("is-active");
    $(".navbar-menu").removeClass("is-active");
  });

  $(".navbar-menu, .dropdown-menu").on("click", function (e) {
    e.stopPropagation();
  });

  $("#toggleSidebar").on("click", function () {
    $("#sidebar").toggleClass("is-hidden-mobile");
  });

  $(window).on("resize", function () {
    if ($(window).width() >= 769) {
      $("#sidebar").removeClass("is-hidden-mobile");
    }
  });

  updateTotal();

  $(".quantity-input").on("input", function () {
    if (parseInt($(this).val()) < 1) $(this).val(1);
    updateTotal();
  });

  $(".remove-btn").on("click", function () {
    $(this).closest(".cart-item").remove();
    updateTotal();
  });
});

function updateTotal() {
  let total = 0;
  $("#cart-list .cart-item").each(function () {
    const priceText = $(this)
      .find(".subtitle")
      .text()
      .replace("$", "")
      .replace(",", "");
    const price = parseFloat(priceText);
    const quantity = parseInt($(this).find(".quantity-input").val());
    if (!isNaN(price) && !isNaN(quantity)) {
      total += price * quantity;
    }
  });
  $("#total-price").text("$" + total.toFixed(2));
}
