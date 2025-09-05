
    // Prices for each class
    var prices = {
        aerobic: 10,
        pilates: 12,
        trampo: 15,
        zumba: 10,
        ballet: 12,
        gymnastic: 16,
    };

 function calculatePrice() {
    var selectedClass = document.querySelector('input[name="selectedSport"]:checked');
    var selectedHours = document.querySelector('input[name="hours"]:checked');
    var selectedDay = document.querySelector('input[name="day"]:checked');
    if (selectedClass && selectedHours && selectedDay) {
        var selectedClassValue = selectedClass.value;
        var selectedHoursValue = selectedHours.value;
        var price = prices[selectedClassValue];
        if (selectedHoursValue === '2hr') {
            price *= 1.5;
        }

        console.log("Selected class value:", selectedClassValue);
        console.log("Selected hours value:", selectedHoursValue);
        console.log("Price:", price);

        document.getElementById("price").value = price ;
        document.getElementById("purchaseButton").style.display = "block";
    } else {
        alert("Error: One or more selections are missing.");
    }
}
document.getElementById('registration-form').addEventListener('submit', function (event) {
alert('Registered Successfully!');
this.submit(); });
document.getElementById('registration-form1').addEventListener('submit', function (event) {
alert('Registered Successfully!');
this.submit(); });