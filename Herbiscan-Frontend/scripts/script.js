$(document).ready(function () {
  // Smooth scrolling for navigation links

  $(".lower-header a").on("click", function (event) {
    event.preventDefault();

    const target = $(this).attr("href");
    let offset = 0;

    // Use this.id to apply custom offset
    switch (this.id) {
      case "home":
        offset = 0; // Offset for Home Page
        break;
      case "aboutUs":
        offset = 75; // Offset for About Us
        break;
      case "imageUploadsLink":
        offset = -180; // Offset for Image Upload
        break;
      default:
        offset = 0; // Default fallback
    }

    $("html, body").animate(
      {
        scrollTop: $(target).offset().top + offset,
      },
      800
    );
  });

  const $uploadBox = $(".upload-box");
  const $imageInput = $("#imageUpload");
  const $imagePreview = $("#imagePreview");

  function showPreview(file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      $imagePreview.html(`<img src="${e.target.result}" alt="Image Preview">`);
    };
    reader.readAsDataURL(file);
  }

  $uploadBox.on("click", function () {
    $imageInput.click();
  });

  $imageInput.on("change", function () {
    if (this.files && this.files[0]) {
      showPreview(this.files[0]);
    }
  });

  // Drag and drop events
  $uploadBox.on("dragover", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).addClass("dragover");
  });

  $uploadBox.on("dragleave", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).removeClass("dragover");
  });

  $uploadBox.on("drop", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).removeClass("dragover");

    const files = e.originalEvent.dataTransfer.files;
    if (files.length > 0) {
      $imageInput[0].files = files; // Assign dropped file to input
      showPreview(files[0]);
    }
  });
});
