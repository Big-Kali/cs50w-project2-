$(document).ready(function () {
  sokectio = io();
  var nombres_array = location.pathname.split("/");
  sokectio.on(
    nombres_array[nombres_array.length - 1],
    function (listas_canales) {
      var canales_get = document.querySelector("#listas-mensajes");
      canales_get.textContent = "";
      var tiempo = new Date();
      //console.log(listas_canales);
      for (const canal of listas_canales) {
        var p = document.createElement("p");
        p.textContent = canal.name + " Dice:" + canal.text + " Enviado " +  tiempo ;
        canales_get.append(p);
         canal.text.on('click',function(){
           canal.text.remove();
        })
      }
    }
  );
  $("#evento_submit").on("submit", function (e) {
    e.preventDefault();
    var dato_form = new FormData($("#evento_submit")[0]);
    dato_form.append("nombre", e.currentTarget.dataset.canal);
    fetch("/menssage", { method: "POST", body: dato_form })
      .then((data) => data.json())
      .then((mensaje) => {
        console.log(mensaje);
        if (!mensaje.error) {
          sokectio.emit("cargar", nombres_array[nombres_array.length - 1]);
        }
      });
  });
  
});
