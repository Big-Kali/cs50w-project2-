$(document).ready(function () {
  var socket = io();
  // var socket_messages = io('http://127.0.0.1:5000/messages');

  socket.emit("listar_canales");
  $("#private-canal-form").on("submit", function (e) {
    e.preventDefault();
    var canal_private = $("#canal").val();
    var form_unico = new FormData($("#private-canal-form")[0]);
    fetch("/canal_unico", { method: "POST", body: form_unico })
      .then((data) => data.json())
      .then((canal) => {
        if (canal.completado) {
          alert("adding");
          socket.emit("listar_canales");
        } else {
          alert("#Ya existe");
        }
      });
  });

  socket.on("private_user", function (data) {
    console.log(data);
  });

  socket.emit("usuario");

  $("#users").on("submit", function (e) {
    e.preventDefault();
    let nombre = $("#nickname").val();
    //debugger
    var dato_form = new FormData($("#users")[0]);
    // debugger
    fetch("/register", { method: "POST", body: dato_form })
      .then((data) => data.json())
      .then((users) => {
        if (users.existente == true) {
          alert("el usuario ya existe, crea otro usuario");
        } else {
          localStorage.setItem("nombre", document.cookie.split("=")[1]);
          //
          var name = localStorage.getItem("nombre");
          document.querySelector("#name-box").innerHTML = name;
          window.location.reload();
        }
      })
      .catch((error) => console.log(error + "hay un error aqui"));
  });

  socket.on("register_ok", function (existente) {
    console.log(existente);
  });

  socket.on("send_canal", function (canaless) {
    console.log(canaless);
    var box_canales = document.querySelector("#canales-box");
    box_canales.innerHTML = " ";
    for (const canal of canaless) {
      var p = document.createElement("li");
      var l = document.createElement('a');
      
      l.textContent = canal.name;
      l.href= '/canal/'+ canal.name;
      p.append(l);
      box_canales.append(p);
    }
  });
 
});
