document.getElementById("btn_login").addEventListener("click", iniciarSesion);
document.getElementById("btn_register").addEventListener("click", register);
window.addEventListener("resize", anchoPage);

//Declarando variables
var form_login = document.querySelector(".form_login");
var form_register = document.querySelector(".form_register");
var contenedor_login_contenedor = document.querySelector("contenedor_login-register");
var card_login = document.querySelector(".card_login");
var card_rgister = document.querySelector(".card_register");

//FUNCIONES

function anchoPage(){
    if(window.innerWidth > 850){
        card_register.style.display = "block";
        card_login.style.display = "block";
    }else{
        card_register.style.display = "block";
        card_register.style.opacity = "1";
        card_login.style.display = "none";
        form_login.style.display = "block";
        contenedor_login_register.style.left = "0px";
        form_register.style.display = "none";
    }
}

anchoPage();

    function iniciarSesion(){
        if(window.innerWidth < 850){
            form_login.style.display = "block";
            contenedor_login_register.style.left = "10px";
            form_register.style.display = "none";
            card_register.style.display = "1";
            card_login.style.opacity = "0";
        }else{
            form_login.style.display = "block";
            contenedor_login_register.style.left = "0px";
            form_register.style.display = "none";
            card_register.style.display = "block";
            card_login.style.display = "none";
        }
    }

    function register(){
        if(window.innerWidth > 850){
            form_register.style.display = "block";
            contenedor_login_register.style.left = "410px";
            form_login.style.display = "none";
            card_register.style.opacity = "0";
            card_login.style.opacity = "1";
        }else{
            form_register.style.display = "block";
            contenedor_login_register.style.left = "0px";
            form_login.style.display = "none";
            card_register.style.display = "none";
            card_login.style.display = "block";
            card_login.style.opacity = "1";
        }
    }