/**
 * This is called code spagetti, but I don't care for js enough to make it good
 * This reads data from the linked text file and adds it to the posts id
 */
$('link[data-src]').each(function(){
	// Reads from file
    var self = $(this), src = self.attr('data-src');
	
	// Gets file data
    $.get(src, function(fileContent){
		// Splits each line
		fileContent = fileContent.slice(0, -1)
		words = fileContent.split("\n");
		words.forEach(element => {

			// Splits data at ,
			data = element.split("::");

			// Creates div that gets data added to it
			var div = document.createElement("div");
			div.className = "post";

			// Creates the title data <p> gives it title classname and adds title text to it
			var title = document.createElement("p");
			title.className = "title";
			title.innerHTML = data[0];

			// Creates the text data <p> gives text classname and adds data
			var text = document.createElement("p");
			text.className = "text";
			text.innerHTML = data[1];

			// Adds title and text to div
			div.appendChild(title);
			div.appendChild(text);

			// Creates anchor
			var anchor = document.createElement("a");
			anchor.href = data[2];

			anchor.appendChild(div);

			// Adds div to posts lists 
			document.getElementById("posts").appendChild(anchor);
			

		});
    })
});