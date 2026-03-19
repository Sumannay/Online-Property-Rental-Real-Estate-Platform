// ================= IMAGE SLIDER (DYNAMIC - PROPERTY BASED) =================

let index = 0;
let images = [];
let sliderInterval = null;

// ✅ Start slider using DB images
function startSlider(img1, img2, img3) {
  images = [];

  if (img1) images.push("/static/uploads/" + img1);
  if (img2) images.push("/static/uploads/" + img2);
  if (img3) images.push("/static/uploads/" + img3);

  if (images.length === 0) return;

  index = 0;

  let slide = document.getElementById("slide");
  if (!slide) return;

  slide.src = images[index];

  // ✅ clear previous interval (important fix)
  if (sliderInterval) {
    clearInterval(sliderInterval);
  }

  sliderInterval = setInterval(function () {
    nextSlide();
  }, 3000);
}

// ================= MANUAL CONTROLS =================

function showImage() {
  let slide = document.getElementById("slide");
  if (!slide || images.length === 0) return;
  slide.src = images[index];
}

function nextSlide() {
  if (images.length === 0) return;

  index++;
  if (index >= images.length) index = 0;

  showImage();
}

function prevSlide() {
  if (images.length === 0) return;

  index--;
  if (index < 0) index = images.length - 1;

  showImage();
}

// ================= DEFAULT SLIDER (OPTIONAL FALLBACK) =================

// if you want static images (homepage etc.)
let defaultImages = [
  "/static/uploads/1.jpg",
  "/static/uploads/2.jpg",
  "/static/uploads/3.jpg",
];

function startDefaultSlider() {
  if (defaultImages.length === 0) return;

  images = defaultImages;
  index = 0;

  let slide = document.getElementById("slide");
  if (!slide) return;

  slide.src = images[index];

  if (sliderInterval) {
    clearInterval(sliderInterval);
  }

  sliderInterval = setInterval(function () {
    nextSlide();
  }, 3000);
}

// ================= FORM VALIDATION =================

function validateForm() {
  let price = document.getElementById("price");
  let contact = document.getElementById("contact");
  let location = document.getElementById("location");

  if (!price || !contact || !location) return true;

  let priceVal = price.value.trim();
  let contactVal = contact.value.trim();
  let locationVal = location.value.trim();

  // ✅ Price validation
  if (!/^\d+$/.test(priceVal)) {
    alert("❌ Please enter valid price (numbers only)");
    return false;
  }

  // ✅ Contact validation
  if (!/^\d{10}$/.test(contactVal)) {
    alert("❌ Enter valid 10-digit contact number");
    return false;
  }

  // ✅ Location validation
  if (!/^[A-Za-z ]+$/.test(locationVal)) {
    alert("❌ Location should contain only letters");
    return false;
  }

  return true;
}

// ================= AUTO LOAD =================

window.onload = function () {
  // Try dynamic slider first
  if (images.length === 0) {
    startDefaultSlider(); // fallback
  }
};
