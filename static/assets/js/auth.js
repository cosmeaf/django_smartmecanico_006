// auth.js
const BASE_API = "http://85.31.231.240:8001/api"
const BASE_URL = "http://85.31.231.240:8001"

// Autehntication Login
document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("login-form");
  
    loginForm.addEventListener("submit", async function (event) {
      event.preventDefault();
  
      const formData = new FormData(loginForm);
  
      try {
        const response = await fetch(`${BASE_URL}/login/`, {
          method: "POST",
          body: formData,
          headers: {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
          },
        });
  
        if (response.ok) {
          const responseData = await response.json();
  
          if (responseData.status === "success") {
            alert("Login bem-sucedido. Bem-vindo!");
            window.location.href = responseData.redirect_url;
          } else {
            alert("Falha no login. Verifique suas credenciais.");
          }
        } else {
          console.error("Erro na resposta do servidor:", response.statusText);
        }
      } catch (error) {
        console.error("Erro ao enviar dados de login:", error);
      }
    });
  
});
  

