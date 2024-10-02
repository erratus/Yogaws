document.getElementById('openModal').addEventListener('click', function(event) {
    event.preventDefault();
    document.getElementById('modal').style.display = 'flex';
});

document.querySelector('.close-button').addEventListener('click', function() {
    document.getElementById('modal').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target === document.getElementById('modal')) {
        document.getElementById('modal').style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('nav');
    let lastScrollTop = 0;

    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > lastScrollTop) {
            // User is scrolling down
            navbar.classList.add('hide');
        } else {
            // User is scrolling up
            navbar.classList.remove('hide');
        }

        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop; // For mobile or negative scrolling
    });
});

function validateForm() {
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirmpassword").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return false;
    } else {
        return true;
    }
}

document.getElementById('video-container').addEventListener('click', function() {
    const videoContainer = this;
  
    // Toggle full screen mode
    if (!videoContainer.classList.contains('fullscreen')) {
      videoContainer.classList.add('fullscreen');
    } else {
      videoContainer.classList.remove('fullscreen');
    }
  });
  
  // Close button functionality
  document.getElementById('close-btn').addEventListener('click', function(event) {
    event.stopPropagation(); // Prevent triggering the fullscreen toggle
    const videoContainer = document.getElementById('video-container');
    videoContainer.style.display = 'none'; // Hide the video container
  });
  