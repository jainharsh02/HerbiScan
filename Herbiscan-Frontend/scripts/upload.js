$(document).ready(function () {
  $("#uploadForm").on("submit", function (e) {
    e.preventDefault();

    const fileInput = $("#imageUpload")[0];
    if (fileInput.files.length === 0) {
      alert("Please upload an image!");
      return;
    }

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    $.ajax({
      url: "https://herbiscan.onrender.com/predict", // Update this to your backend URL if hosted
      type: "POST",
      data: formData,
      processData: false,
      contentType: false,
      success: function (response) {
        //   $('#imagePreview').append(`<p><strong>Prediction:</strong> ${response.label}</p>`);
        // $('#imagePreview').append(`<p><strong>Prediction:</strong> ${response.predicted_class}</p>`);

        // const detailsHtml = `
        // <p><strong>Prediction:</strong> ${response.prediction}</p>
        // <p><strong>Medicinal Benefit:</strong> ${response.benefit}</p>
        // <p><strong>Soil Type:</strong> ${response.soil}</p>
        // <p><strong>Color & Vein Pattern:</strong> ${response.appearance}</p>
        // <p><strong>Region Found:</strong> ${response.region}</p>
        // `;

        const detailsHtml = `
          
          <div class="results-wrapper">
            <h2 class="line-sec">${response.prediction}</h2>
            <h3>
              Plant's Medicinal Benefit<br />
              <span class="small">
              ${response.benefit}.
              </span>
            </h3>
            <h3>
              Soil Type<br />
              <span class="small"> ${response.soil} </span>
            </h3>
            <h3>
              Color & Vein Pattern<br />
              <span class="small"> ${response.appearance} </span>
            </h3>
            <h3>
              Region Found<br />
              <span class="small"> ${response.region} </span>
            </h3>
          </div>

        `;

        $("#img-result").append(detailsHtml);
      },
      error: function (xhr, status, error) {
        console.error("Error:", error);
        $("#imagePreview").append(
          `<p style="color:red;">Error: ${xhr.responseText}</p>`
        );
      },
    });
  });

  $("#imageUpload").on("change", function () {
    const file = this.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        $("#imagePreview").html(
          `<img src="${e.target.result}" style="max-width: 300px;" />`
        );
      };
      reader.readAsDataURL(file);
    }
  });
});
