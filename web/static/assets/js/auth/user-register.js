// auth.js
const BASE_API = "http://85.31.231.240:8001/api"
const BASE_URL = "http://85.31.231.240:8001"

// Autehntication Login
document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("register-form");
  
    form.addEventListener("submit", async function (event) {
      event.preventDefault();
  
      const formData = new FormData(form);
  
      const response = await fetch(`${BASE_URL}/register/`, {
        method: "POST",
        body: formData,
        headers: {
          "Accept": "application/json",
          "X-Requested-With": "XMLHttpRequest",
        },
      });
      try {
        if (!response.ok) {
          const responseData = await response.json();
          const status = responseData.status;
          let errorMessages = [];
      
          for (let field in responseData.errors) {
              errorMessages.push(responseData.errors[field].join(", "));
          }
          alert(errorMessages.join("; "))
          return {
              status: status,
              data: errorMessages.join("; ")
          };
      }else if (response.ok){
        const responseData = await response.json();

        if (responseData.status === "success") {
          alert("Registro realizado com sucesso!");
          window.location.href = responseData.redirect_url;
        } else {
          alert("Falha no login. Verifique suas credenciais.");
        }

      }
      
      
      } catch (error) {
        console.log(error)
      }
    });
  });
  

