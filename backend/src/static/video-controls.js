!function () {
  document.addEventListener('DOMContentLoaded', function () {
    /** @type {HTMLVideoElement} */
    const video = document.querySelector('.embed-video');
    const videoControls = document.querySelector('.video-controls')
    const volumeToggle = videoControls?.querySelector('.video-volume-toggle');
    /** @type {HTMLInputElement} */
    const volumeSlider = videoControls?.querySelector('.video-volume-slider input');
    const fullscreenToggle = videoControls?.querySelector('.video-fullscreen');
    let lastVolume = 50;

    if (!video || !volumeToggle || !volumeSlider || !fullscreenToggle) {
      console.error('Can\'t continue, missing element - video:', video, 'volume toggle:', volumeToggle, 'slider:', volumeSlider, 'fullscreen toggle:', fullscreenToggle);
      return;
    }

    if (video.muted) {
      volumeToggle.classList.add('muted');
      volumeSlider.value = '0';
    }

    video.addEventListener('volumechange', function () {
      const volume = video.muted ? 0 : video.volume * 100;
      volumeSlider.value = volume;
      if (volume === 0) {
        volumeToggle.classList.add('muted');
        volumeToggle.classList.remove('above_50');
      } else {
        volumeToggle.classList.remove('muted');
        if (volume > 50) {
          volumeToggle.classList.add('above_50');
        } else {
          volumeToggle.classList.remove('above_50');
        }
      }
    });

    // Event Listener for Volume Slider
    volumeSlider.addEventListener('input', function () {
      let volume = volumeSlider.value / 100;
      video.volume = volume;
      if (video.muted && volume > 0) {
        video.muted = false;
      }
      if (volume <= 0) {
        lastVolume = 50;
      }
    });

    // Event Listener for Volume Toggle
    volumeToggle.addEventListener('click', function () {
      const muted = video.muted;
      if (!muted && video.volume == 0) {
        video.volume = 0.5;
      } else {
        video.muted = !muted;
      }
    });

    // Event Listener for Fullscreen Toggle
    fullscreenToggle.addEventListener('click', async function () {
      if (video.requestFullscreen) {
        await video.requestFullscreen();
      } else if (video.mozRequestFullScreen) { // Firefox
        video.mozRequestFullScreen();
      } else if (video.webkitRequestFullscreen) { // Chrome, Safari and Opera
        video.webkitRequestFullscreen();
      } else if (video.msRequestFullscreen) { // IE/Edge
        video.msRequestFullscreen();
      }
    });
  });
}();
