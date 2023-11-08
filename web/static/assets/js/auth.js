// auth.js
const BASE_API = "http://85.31.231.240:8001/api"
const BASE_URL = "http://85.31.231.240:8001"

// Autehntication Login
document.getElementById('login-form').addEventListener('submit', async function(e) {
  e.preventDefault();

  var data = new FormData(this);

  try {
      const response = await fetch(this.action, {
          method: 'POST',
          headers: {
              'X-CSRFToken': getCookie('csrftoken')  
          },
          body: data 
      });

      if (response.ok) {
          window.location.href = '/some-success-url';
      } else {

          alert('Login failed!');
      }
  } catch (error) {
      console.error('Error:', error);
  }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

