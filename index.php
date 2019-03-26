
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <title>Widget Page!</title>
  </head>
  <body>
    <h1>Widget Page!</h1>

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
    
    <style>
    #newComputerForm{
        max-width: 700px;
    }
    .card{
        max-width: 500px;
        margin: 20px;
    }
    </style>
    
    
    <form id="newComputerForm">
      <div class="form-group row">
        <label for="colFormLabel" class="col-sm-2 col-form-label">Computer Name</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="computerNameFormField" placeholder="JOHN-DESKTOP">
        </div>
      </div>
      <div class="form-group row">
        <label for="colFormLabel" class="col-sm-2 col-form-label">Computer IP Address</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="computerIPFormField" placeholder="192.168.1.43">
        </div>
      </div>
      <div class="form-group row">
        <label for="colFormLabel" class="col-sm-2 col-form-label">Computer MAC Address</label>
        <div class="col-sm-10">
          <input type="text" class="form-control" id="computerMACFormField" placeholder="00-14-22-01-23-45">
        </div>
      </div>
      <button type="submit" class="btn btn-primary">Save Computers</button>
    </form>
    
    <div id="cards">
        <div class="card">
            <div class="card-body">
                <div class="container">
                    <div class="row"> 
                        <div class="col-8">
                            <h5 class="card-title">Card title</h5>
                            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
                        </div>
                        <div class="col-4">
                        <a href="#" class="btn btn-primary">Go somewhere</a>
                        </div>
                    </div>
                </div>
                
                
            </div>
        </div>
    </div>
    
    <?php
    
    // > PHP 5
    // $file = file_get_contents('./computers.json', FILE_USE_INCLUDE_PATH);
    //echo $file;
    
    try {
        // $fh = fopen("computers.json", "r");
        $fh = file_get_contents('./computers.json', FILE_USE_INCLUDE_PATH);
        if (! $fh) {
            throw new Exception("Could not open the file!");
        }
        // print_r($fh);
    }
    catch (Exception $e) {
        // echo "Error (File: ".$e->getFile().", line ".
        //       $e->getLine()."): ".$e->getMessage();
        $fh = null;
        
    }
    
    
    ?>
    
    
    
    <script>
    var computersFileData = null;
    
    computersFileData = <?php if ($fh) { echo $fh; } else { echo "null"; } ?>;
    
    if (computersFileData == "null"){ computersFileData = null;}
    
    console.log(computersFileData);
    
    document.getElementById("newComputerForm").addEventListener("submit", saveComputers);
    
    populateComputerCards(computersFileData);

    // populate the list of existing computers
    function populateComputerCards(computersFileData){
        var cards = document.getElementById("cards");
        
        for (comp in computersFileData){
            
            var title = document.createElement("h5");
            title.classList.add("card-title");
            title.innerText = computersFileData[comp]["name"];

            var text = document.createElement("p");
            text.classList.add("card-text");
            text.innerText = computersFileData[comp]["mac"];

            var button = document.createElement("a");
            button.classList.add("btn", "btn-primary");
            button.innerText = "Wake";
            button.href = "#";

            var cardBody = document.createElement("div");
            cardBody.classList.add("card-body");

            cardBody.appendChild(title);
            cardBody.appendChild(text);
            cardBody.appendChild(button);

            var card = document.createElement("div");
            card.classList.add("card");
            
            card.appendChild(cardBody);

            cards.appendChild(card);

        }
        

    }

    function saveComputers() {
        //   alert("The form was submitted");

        newComputerForm = document.forms["newComputerForm"];

        newComputerFormData = {};
        newComputerFormData["name"] = newComputerForm["computerNameFormField"].value
        newComputerFormData["ip"] = newComputerForm["computerIPFormField"].value
        newComputerFormData["mac"] = newComputerForm["computerMACFormField"].value

        console.log(newComputerFormData);

        console.log(newComputerForm["computerNameFormField"].value);

        //   if there is no pre-existing data on configured computers, initialize the variable
        if(!computersFileData){
            console.log("`computersFileData` is empty...")
            
            computersFileData = [
                {"name":"JOHN-DESKTOP",
                "ip":"192.168.1.43",
                "mac":"00-14-22-01-23-45"
                }]
            
            
            
        }
        else{

            // check if the current entry is already a saved entry
            isNewEntry = true;
            for (comp in computersFileData){

                if (comp["mac"] == newComputerFormData["mac"]){
                    isNewEntry = false;

                    comp["name"] = newComputerFormData["name"];
                    comp["ip"] = newComputerFormData["ip"];

                }

            }
            if (isNewEntry){
                computersFileData.push(newComputerFormData)
                
            }
            console.log(computersFileData)

        }
        
        var url = "index.php";
            
        var jsonComputerData = JSON.stringify(computersFileData);
        console.log(jsonComputerData)
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        xhr.setRequestHeader('Content-type','application/json; charset=utf-8');
        // // xhr.onload = function () {
        // // 	var response = JSON.parse(xhr.responseText);
        // // 	if (xhr.readyState == 4 && xhr.status == "201") {
        // // 		console.log(response);
        // // 	} else {
        // // 		console.error(response);
        // // 	}
        // // }
        xhr.send(jsonComputerData);
      
    }
    </script>
    
    <?php
    $data = file_get_contents('php://input');
    echo $data;
    file_put_contents("computers1.json",$data);
    
    ?>
    
    
  </body>
</html>