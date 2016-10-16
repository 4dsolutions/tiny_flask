/**
 * 
 */
function sponsored_by () {
	var sponsor = "<a href='http://www.4dsolutions.net'><i>4D Solutions</i></a>"
	document.getElementById("sponsor").innerHTML = "Brought to you by " + sponsor;
}

function goHome() {
	window.location = "/home";
}

function goTerms() {
	window.location = "/glossary";
}

function goElements() {
	window.location = "/elements";
}

function goShapes() {
	window.location = "/shapes";
}

function SubmitMe() {
	var the_form = document.getElementById("the_form");
	the_form.submit();
	var edit_button = document.getElementById("Edit");
	edit_button.style.backgroundColor = "blue";
	edit_button.setAttribute( "onClick", "javascript: EditMe();");
	var delete_button = document.getElementById("Submit");
	delete_button.innerHTML = "Delete";
	delete_button.setAttribute( "onClick", "javascript: DeleteMe();");
	delete_button.setAttribute("id", "Delete");
	delete_button.style.backgroundColor = "blue";
	var add_button = document.getElementById("Cancel");
	add_button.innerHTML = "Add";
	add_button.style.backgroundColor = "blue";
	add_button.setAttribute( "onClick", "javascript: AddMe();");
	add_button.setAttribute("id", "Add");	
	var x = document.getElementsByClassName("editable");
	var i;
	for (i = 0; i < x.length; i++) {
	    x[i].setAttribute("disabled", "disabled");
	}

}

function CancelMe() {
	var edit_button = document.getElementById("Edit");
	edit_button.style.backgroundColor = "blue";
	edit_button.setAttribute( "onClick", "javascript: EditMe();");
	var delete_button = document.getElementById("Submit");
	delete_button.innerHTML = "Delete";
	delete_button.setAttribute( "onClick", "javascript: DeleteMe();");
	delete_button.setAttribute("id", "Delete");
	delete_button.style.backgroundColor = "blue";
	var add_button = document.getElementById("Cancel");
	add_button.innerHTML = "Add";
	add_button.style.backgroundColor = "blue";
	add_button.setAttribute( "onClick", "javascript: AddMe();");
	add_button.setAttribute("id", "Add");
	var x = document.getElementsByClassName("editable");
	var i;
	for (i = 0; i < x.length; i++) {
	    x[i].setAttribute("disabled", "disabled");
	}
}

function EditMe() {
	var edit_button = document.getElementById("Edit");
	edit_button.setAttribute( "onClick", "" );;
	edit_button.style.backgroundColor = "#e7e7e7";
	var delete_button = document.getElementById("Delete");
	delete_button.style.backgroundColor = "green";
	delete_button.innerHTML = "Submit";
	delete_button.setAttribute( "onClick", "javascript: SubmitMe();" );
	delete_button.setAttribute("id", "Submit");
	var add_button = document.getElementById("Add");
	add_button.style.backgroundColor = "red";
	add_button.innerHTML = "Cancel";
	add_button.setAttribute( "onClick", "javascript: CancelMe();" );
	add_button.setAttribute("id", "Cancel");
	var x = document.getElementsByClassName("editable");
	var i;
	for (i = 0; i < x.length; i++) {
	    x[i].removeAttribute("disabled");
	}
}