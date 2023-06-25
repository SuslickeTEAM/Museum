document.addEventListener("DOMContentLoaded", function() {
  const panoramaImage = new PANOLENS.ImagePanorama("static/images/1.jpg");
  const masthead = document.querySelector(".masthead");
  const panoramaContainer = document.querySelector("#panorama");

  const viewer = new PANOLENS.Viewer({
    container: panoramaContainer,
    autoRotate: true,
    autoRotateSpeed: 0.3,
    controlBar: false,
    autoRotateActivationDuration: 5000,
  });

  viewer.add(panoramaImage);

  masthead.style.background = "url('static/images/1.jpg')";

  viewer.container.addEventListener('mousedown', () => {
    viewer.autoRotate = false;
    clearTimeout(viewer.autoRotateTimeout);
    viewer.autoRotateTimeout = setTimeout(() => {
      viewer.autoRotate = true;
    }, viewer.autoRotateActivationDuration);
  });
});

var heading = document.querySelector('.display-1');
var paragraph = document.querySelector('.intro-text');

function hideText() {
  heading.style.opacity = '0';
  paragraph.style.opacity = '0';
}

function showText() {
  heading.style.opacity = '1';
  paragraph.style.opacity = '1';
}

setTimeout(hideText, 5000);