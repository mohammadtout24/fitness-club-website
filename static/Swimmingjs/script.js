
$(document).ready(function () { // .ready() After loading page 
    'use strict';
    $(window).scroll(function () { // .scroll() While scrolling
        'use strict';
        if ($(window).scrollTop() < 300) // Before reaching the head-section
        {
            // Hide Up Arrow
            $('.up-arrow').css({
                'opacity': '0'
            });
        } else {
            // Show Up Arrow
            $('.up-arrow').css({
                'opacity': '1'
            });
        }
    });
});

// Initalization of Wow from Animate

$(document).ready(function(){
    'use strict';
    
    new WOW().init();
});

function calculatePrice() {
    const membership = document.getElementById("membership").value;
    const ageRange = document.getElementById("age-range").value;
    
    let basePrice = 0;
    
    // Set default base prices for each scenario
    const basePrices = {
        weekly: {
            baby: 20,
            kid: 30,
            adult: 40
        },
        monthly: {
            baby: 40,
            kid: 60,
            adult: 80
        },
        yearly: {
            baby: 140,
            kid: 210,
            adult: 280
        }
    };
    
    // Set base price based on selected membership and age range
    basePrice = basePrices[membership][ageRange];

    console.log("Selected age-range value:", ageRange);
    console.log("Selected plan value:", membership);
    console.log("Base Price:", basePrice);

    document.getElementById("price").value = basePrice;
}
function hello() {
    console.log("I am being clicked");
}