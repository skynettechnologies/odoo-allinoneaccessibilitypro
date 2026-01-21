// =======================
// RADIO GROUP INITIAL SETUP
// =======================

var radiogroups = document.querySelectorAll('div[role="radiogroup"]');

if (radiogroups.length >= 2) {
    var radiogroup1 = radiogroups[0]
        .querySelector("input[type='radio']")
        .getAttribute("name");

    var radiogroup2 = radiogroups[1]
        .querySelector("input[type='radio']")
        .getAttribute("name");

    // =======================
    // ICON TYPE OPTIONS
    // =======================

    var element1 = document.querySelectorAll(
        'input[name="' + radiogroup1 + '"]'
    );

    var total = 0;

    element1.forEach(function (img) {
        total += 1;
        var next = img.nextElementSibling;

        var icon = document.createElement("img");
        icon.src = "https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-" + total + ".svg";
        icon.height = 55;
        icon.width = 55;

        next.append(icon);
    });

    // =======================
    // ICON SIZE OPTIONS
    // =======================

    var element2 = document.querySelectorAll(
        'input[name="' + radiogroup2 + '"]'
    );

    var selectedType = document.querySelector(
        'input[name="' + radiogroup1 + '"]:checked'
    );

    var value_total = 85;

    element2.forEach(function (img) {
        value_total -= 10;
        var next = img.nextElementSibling;

        var icon = document.createElement("img");

        if (selectedType === null) {
            icon.src = "https://www.skynettechnologies.com/sites/default/files/aioa-icon-type-1.svg";
        } else {
            icon.src =
                "https://www.skynettechnologies.com/sites/default/files/" +
                selectedType.getAttribute("data-value") +
                ".svg";
        }

        icon.height = value_total;
        icon.width = value_total;
        icon.className = "csticontype";

        next.append(icon);
    });

    // =======================
    // CHANGE ICON TYPE ON CLICK
    // =======================

    var sizeOptionsImg = document.querySelectorAll(".csticontype");
    var typeOptions = document.querySelectorAll(
        'input[name="' + radiogroup1 + '"]'
    );

    typeOptions.forEach(function (option) {
        option.addEventListener("click", function () {
            var ico_type = document
                .querySelector(
                    'input[name="' + radiogroup1 + '"]:checked'
                )
                .getAttribute("data-value");

            sizeOptionsImg.forEach(function (img) {
                img.setAttribute(
                    "src",
                    "https://www.skynettechnologies.com/sites/default/files/" + ico_type + ".svg"
                );
            });
        });
    });
}

// // =======================
// // SAVE DATA FUNCTION
// // =======================

// function saveData(e) {
//     e.preventDefault();

//     var server_name = window.location.origin;
//     var color = document.querySelector(".aioa_color_code_pro").value;
//     var position = document.querySelector(".place_pro").value;
//     var icon_type = document.querySelector(".aioa_icon_type_pro").value;
//     var icon_size = document.querySelector(
//         ".aioa_icon_size_desktop_pro"
//     ).value;

//     var request = new XMLHttpRequest();
//     var url = "https://www.skynettechnologies.com/sites/default/files/widget-setting-update-platform";

//     var params =
//         "u=" +
//         encodeURIComponent(server_name) +
//         "&widget_position=" +
//         encodeURIComponent(position) +
//         "&widget_color_code=" +
//         encodeURIComponent(color) +
//         "&widget_icon_type=" +
//         encodeURIComponent(icon_type) +
//         "&widget_icon_size=" +
//         encodeURIComponent(icon_size);

//     request.open("POST", url, true);
//     request.setRequestHeader(
//         "Content-type",
//         "application/x-www-form-urlencoded"
//     );

//     request.onreadystatechange = function () {
//         if (
//             request.readyState === XMLHttpRequest.DONE &&
//             request.status === 200
//         ) {
//             console.info("save data");
//         }
//     };

//     request.send(params);
//     return true;
// }
