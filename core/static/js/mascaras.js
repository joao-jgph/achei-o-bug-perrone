$(document).ready(function($)
{	
    // CPF
	$('.cpf').mask("999.999.999-99", {autoclear: false});

    // CPNJ
	$(".cnpj").mask("99.999.999/9999-99");

    // RG
	$(".rg").mask("99.999.999-99", {autoclear: false})
	
    // CELULAR
	$('.celular').mask("(99) 99999-9999", {autoclear: false});

    // TELEFONE
	$('.telefone').mask("(99) 9999-9999", {autoclear: false});

    // DATA
	$(".data").mask("99/99/9999");

    // HORA
	// $(".hora").mask("99:99:99");

    // ANO 
    $(".mascara-ano").mask("9999", {autoclear: false})

    // CEP
    $('.cep').mask("99.999-999", {autoclear: false});

}); 
