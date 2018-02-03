function submitFunc(event){
        console.log("Hey what are you looking for? ")
        event.preventDefault();
        obj = {
            MRN: $("#MRN").val(),
            year: $("#year").val(),
            month: $("#month").val(),
            day: $("#day").val(),
            hour: $("#hour").val(),
            minute: $("#minute").val(),
            Dept: $("#Dept").val(),
            Practice: $("#Practice").val()
        };
        console.log(obj)

        $.ajax({
        url:"/search/info/api",
        type:"POST",
        contentType: "application/json",
        dataType:"json",
        data: JSON.stringify(obj),
        success:function(data){
            $("#table").remove();
            var cols = ["date"];
            for(var i = 7; i <= 19; ++i) {
                cols.push(i);
            }
            console.log(cols)
            $("#result_table").append(createTable(data, cols));
        }}
        );    
    }

    function createTable(input, cols){
        console.log(input);
        var table = document.createElement("table");
        table.classList.add("chart");
        table.id = "table"
        table.appendChild(createRow(cols,"label"));
        for(var data in input){
            var arr = Object.values(input[data]);
            arr.unshift(data);
            table.appendChild(createRow(arr,"row"));
        }
        return table;
    }

    function createRow(input,className){
        var row = document.createElement("tr");
        for(var item of input){
            var cell = document.createElement("th");
            cell.classList.add(className);
            cell.classList.add("cell");
            if(!isNaN(item) && item > 0.4 && item <= 1){
                var num = Math.pow((item - 0.3)/0.7, 2) * 255;
                cell.style.color = "rgb(" + Math.round(num) + ",0,0)";
                // cell.style.color = "#CCCCCC";
            }
            var cellText = document.createTextNode(item);
            cell.appendChild(cellText)
            row.appendChild(cell);
        }
        row.childNodes[0].classList.add("date");
        return row;
    }
















