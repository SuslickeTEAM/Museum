document.addEventListener("DOMContentLoaded", function () {
    const panoramaImage = new PANOLENS.ImagePanorama("static/images/1.jpg");
    const panoramaContainer = document.querySelector("#panorama");

    const viewer = new PANOLENS.Viewer({
        container: panoramaContainer,
        autoRotate: true,
        autoRotateSpeed: 0.3,
        controlBar: false,
        autoRotateActivationDuration: 5000,
    });

    viewer.add(panoramaImage);

    // Панорама активна и реактивируется после взаимодействия
    viewer.container.addEventListener('mousedown', () => {
        viewer.autoRotate = false;
        clearTimeout(viewer.autoRotateTimeout);
        viewer.autoRotateTimeout = setTimeout(() => {
            viewer.autoRotate = true;
        }, viewer.autoRotateActivationDuration);
    });

    // Скрытие текста через 5 секунд
    setTimeout(() => {
        document.getElementById('heading').classList.add('fade-out');
        document.getElementById('paragraph').classList.add('fade-out');
    }, 5000);
});
