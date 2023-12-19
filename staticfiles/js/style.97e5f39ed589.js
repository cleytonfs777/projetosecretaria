function formatToCurrency(element) {
    let input = element.value;
    input = input.replace(/[\D]/g, ""); // Remove tudo que não é número
    input = input.replace(/(\d)(\d{2})$/, "$1,$2"); // Coloca vírgula antes dos últimos 2 dígitos
    input = input.replace(/(?=(\d{3})+(\D))\B/g, "."); // Coloca ponto a cada 3 dígitos
    if(input == '' || input == 0){
        element.value = "";
    }else{
        element.value = `R$ ${input}`;
    }
  }

function calcMedia() {
    let nota1 = parseFloat(document.getElementById("val1Item").value == "" ? 0 : document.getElementById("val1Item").value.replace("R$ ", "").replace(".", "").replace(",", "."));
    let nota2 = parseFloat(document.getElementById("val2Item").value == "" ? 0 : document.getElementById("val2Item").value.replace("R$ ", "").replace(".", "").replace(",", "."));
    let nota3 = parseFloat(document.getElementById("val3Item").value == "" ? 0 : document.getElementById("val3Item").value.replace("R$ ", "").replace(".", "").replace(",", "."));
    let cont = 0;
    
    if (nota1 != 0) {
        cont++;
    }
    if (nota2 != 0) {
        cont++;
    }
    if (nota3 != 0) {
        cont++;
    }
    let media = (nota1 + nota2 + nota3) / cont;
    media = media.toFixed(2);
    //Tratamento para quando o usuário não digitar nada
    media = String(media);
    media = media.replace(/[\D]/g, ""); // Remove tudo que não é número
    media = media.replace(/(\d)(\d{2})$/, "$1,$2"); // Coloca vírgula antes dos últimos 2 dígitos
    media = media.replace(/(?=(\d{3})+(\D))\B/g, "."); // Coloca ponto a cada 3 dígitos

    document.getElementById("valMedItem").value = `R$ ${media}`;
}

function removerElemento(elementoClicado) {
    var tr = elementoClicado.parentNode.parentNode;
    tr.parentNode.removeChild(tr);
  }

function converterParaFormatoBrasileiro(dataISO) {
  // Cria um objeto de data a partir da string ISO
  var data = new Date(dataISO);

  // Formata o dia, mês, ano, hora e minuto
  var dia = String(data.getUTCDate()).padStart(2, '0');
  var mes = String(data.getUTCMonth() + 1).padStart(2, '0'); // Janeiro é 0!
  var ano = data.getUTCFullYear();
  var hora = String(data.getUTCHours()).padStart(2, '0');
  var minuto = String(data.getUTCMinutes()).padStart(2, '0');

  // Retorna a data formatada
  return `${dia}/${mes}/${ano} ${hora}:${minuto}`;
}

document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.close-alert');

    closeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const alert = this.parentElement;
            alert.style.display = 'none';
        });
    });
});

function launchErrorDefault(msg, id_tag){
    // inserir um texto de erro do tipo alert-danger no elemnto div de id = 'alert com um x para fechar o alert'
    document.getElementById(id_tag).innerHTML = `<div class="alert alert-danger alert-dismissible fade show" role="alert">\
      <strong>Erro! </strong> ${msg}.\
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
    </div>`;
    }

function launchSuccessDefault(msg, id_tag){
    // inserir um texto de erro do tipo alert-danger no elemnto div de id = 'alert com um x para fechar o alert'
    document.getElementById(id_tag).innerHTML = `<div class="alert alert-success alert-dismissible fade show" role="alert">\
    <strong>Ok! </strong> ${msg}.\
    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>\
    </div>`;
    }

function datasSobrepostas(datahorainit1, datahorafim1, collectlist){
    let resultado = false;
    console.log("datahorainit1", datahorainit1, "Tipo da variável: ", typeof datahorainit1);
    console.log("datahorafim1", datahorafim1, "Tipo da variável: ", typeof datahorafim1);
    
    if(!collectlist) return false;
    
    for(var itt of collectlist){
        resultado = verificaSobreposicaoDatas(datahorainit1, datahorafim1, itt[0], itt[1]);
        console.log("Sobreposição: ", resultado);
        if (resultado) {
            return true;
        }

    }
    return false;
}

function formatarData(dataStr) {
    // Convertendo de DD/MM/YYYY HH:MM para YYYY-MM-DDTHH:MM
    let partes = dataStr.split(" ");
    let data = partes[0].split("/").reverse().join("-");
    let hora = partes[1];
    return data + "T" + hora;
}

function verificaSobreposicaoDatas(dataInicial1, dataFinal1, dataInicial2, dataFinal2) {
    // Convertendo as strings de data para objetos Date após reformatá-las
    let di1 = new Date(formatarData(dataInicial1));
    let df1 = new Date(formatarData(dataFinal1));
    let di2 = new Date(formatarData(dataInicial2));
    let df2 = new Date(formatarData(dataFinal2));

    // Verificando sobreposição
    if (di1 > df2 || df1 < di2) {
        return false; // Não há sobreposição
    } else {
        return true; // Há sobreposição
    }
}

function normalizepostgrad(value) {
    switch (value) {
        case 'sd2cl':
            return 'Sd 2ª Classe BM';
        case 'sd':
            return 'Sd BM';
        case 'cb':
            return 'Cb BM';
        case '3sgt':
            return '3º Sgt BM';
        case '2sgt':
            return '2º Sgt BM';
        case '1sgt':
            return '1º Sgt BM';
        case 'subten':
            return 'Sub Ten BM';
        case '2ten':
            return '2º Ten BM';
        case '1ten':
            return '1º Ten BM';
        case 'cap':
            return 'Cap BM';
        case 'maj':
            return 'Maj BM';
        case 'tencel':
            return 'Ten Cel BM';
        case 'cel':
            return 'Cel BM';
        default:
            return value;
    }
  }
  function normalizeLocal(value) {
    switch (value) {
        case 'acf':
            return 'ACF';
        case 'acf1':
            return 'ACF-1';
        case 'acf2':
            return 'ACF-2';
        case 'acf3':
            return 'ACF-3';
        case 'sdts1':
            return 'SDTS-1';
        case 'sdts2':
            return 'SDTS-2';
        case 'sdts3':
            return 'SDTS-3';
        case 'nts':
            return 'NTS';
        case 'gol':
            return 'GOL';
        case 'sdal':
            return 'SDAL';
        case 'sdal1':
            return 'SDAL-1';
        case 'sdal2':
            return 'SDAL-2';
        case 'sdal3':
            return 'SDAL-3';
        case 'sdal4':
            return 'SDAL-4';
        case 'sec':
            return 'Secretaria';
        default:
            return value;
    }
}

  function minutosParaHoras(minutos) {
    // Calcula as horas e os minutos restantes
    var horas = Math.floor(minutos / 60);
    var minutosRest = minutos % 60;

    // Retorna a string formatada
    return horas.toString().padStart(2, '0') + ':' + minutosRest.toString().padStart(2, '0');
}

function horasParaMinutos(horasStr) {
    // Divide a string de horas em horas e minutos
    var partes = horasStr.split(':');
    var horas = parseInt(partes[0]);
    var minutos = parseInt(partes[1]);

    // Converte tudo para minutos e retorna o total
    return (horas * 60) + minutos;
}

function toggleContent() {
    var content = document.getElementById("content");
    var arrow = document.querySelector(".arrow");

    if (content.style.display === "none") {
        content.style.display = "block";
        arrow.classList.add("expanded");
    } else {
        content.style.display = "none";
        arrow.classList.remove("expanded");
    }
}
